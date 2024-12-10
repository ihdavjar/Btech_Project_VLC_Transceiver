import os
import h5py
import argparse 
import scipy.io
import numpy as np

# Function to check if the matrix is Identity matrix
def is_identity_matrix(matrix):
    """
    Check if the input matrix is an identity matrix.
    """
    rows, cols = matrix.shape
    if rows != cols:
        return False

    # Iterate over the diagonal elements
    for i in range(rows):
        if matrix[i, i] != 1:
            return False
        if sum(matrix[i, :]) != 1:
            return False
    return True

def systematic_form(H):
    """
    Convert the parity check matrix H to systematic form [P | I_p].
    This will ensure that the right part of H is an identity matrix.
    """
    # Perform row operations to convert the last p columns to an identity matrix
    rows, cols = H.shape
    p = rows
    n = cols
    k = n - p  # Number of information bits

    # Separate H into two parts: left P and right I_p (if H is already in systematic form)
    P = H[:, :k]
    I_p = H[:, k:]

    if not is_identity_matrix(I_p):
        # If I_p is not an identity matrix, apply Gaussian elimination to H
        H_sys = H.copy()
        for i in range(p):
            # Make sure we have 1 on the diagonal of I_p
            if H_sys[i, k + i] == 0:
                # Swap rows if the current diagonal element is 0
                for j in range(i + 1, p):
                    if H_sys[j, k + i] == 1:
                        H_sys[[i, j]] = H_sys[[j, i]]  # Swap rows
                        break
            # Eliminate other rows in the current column
            for j in range(p):
                if j != i and H_sys[j, k + i] == 1:
                    H_sys[j] = (H_sys[j] + H_sys[i]) % 2  # XOR operation (binary addition)

        P = H_sys[:, :k]
        I_p = H_sys[:, k:]

    return P, I_p

def generator_matrix(H):
    """
    Calculate the generator matrix G given the parity check matrix H.
    """
    p = H.shape[0]  # Number of parity bits
    n = H.shape[1]  # Total number of bits
    k = n - p       # Number of information bits

    # Get P and I_p from H
    P, I_p = systematic_form(H)

    print(P.shape, I_p.shape)
    
    # Initialize G as a boolean array to save memory
    G = np.zeros((k, k + P.shape[0]), dtype=bool)
    G[:, :k] = np.eye(k, dtype=bool)     # Set the identity matrix part
    G[:, k:] = P.T.astype(bool)          # Set the P.T part directly as boolean
    
    return G

# Write a File name "encoder.v"
def write_encoder_verilog(G, path):
    """
    Write the encoder module in Verilog HDL.
    """
    k, n = G.shape
    with open(path, 'w') as f:
        f.write('module encoder(frame_data, out);\n');
        f.write(f'    input [{k-1}:0] frame_data; // Frame bits\n');
        f.write(f'    output [{n-1}:0] out; // Output encoded bits with parity bits = {n}\n');
        f.write('\n\n')
        
        for i in range(k):
            f.write(f'    assign out[{i+n-k}] = frame_data[{i}];\n')

        f.write('\n\n')

        for i in range(k, n):
            temp_col = G[:, i]
            temp_str_col = ''

            for j in range(k):
                if temp_col[j] == 1:
                    temp_str_col += f'frame_data[{j}] ^ '
            
            temp_str_col = temp_str_col[:-3]
            f.write(f'    assign out[{i-k}] = {temp_str_col};\n')
        
        f.write('\n')
        
        f.write('endmodule\n')


if __name__ == '__main__':

    arg = argparse.ArgumentParser(description='Generate Verilog code for TX')
    arg.add_argument('--path_mat', type=str, default='H_mat_8_24.mat', help='Path to the H matrix')
    arg.add_argument('--path_out', type=str, default='tx_code.v', help='Path to the output file')

    args = arg.parse_args()

    mat_path = args.path_mat
    out_path = args.path_out

    # Load the parity check matrix H
    with h5py.File(mat_path, 'r') as f:
        H_matrix = f['H'][:]  # Reads the dataset 'H' into a NumPy array

    
    # Taking transpose of H matrix
    H_matrix = H_matrix.T

    rows, cols = H_matrix.shape
    print(f"Loaded H matrix of size {rows}x{cols}.")
    
    p = rows
    n = cols
    k = n - p  # Number of information bits

    print(f"Loaded H matrix of size {p}x{n} with {k} information bits and {p} parity bits.")

    # Calculate the generator matrix G
    G_matrix = generator_matrix(H_matrix).astype(np.int8)


    # Making new directory
    if not os.path.exists(os.path.join(out_path, 'verilog_code')):
        os.makedirs(os.path.join(out_path, 'verilog_code'))


    # Write the Verilog code for the TX module

    # write the Enable Control Unit (ECU)
    with open(os.path.join(out_path, 'verilog_code', 'Enable_Control_Unit.v'), 'w') as f:
        f.write('''//// Control Unit for Enable
module Enable_Control_Unit(clk, tx_complete, enable, out_clk);

    parameter div_freq = 2500; // Freq = 12.5MHz/div_freq (According to the sampling frequency)
    
    input clk, tx_complete;
    
    output reg out_clk;
    output wire enable;
    
    reg [31:0] count; // Count register
    
    reg temp_reg;
    
    initial
    begin
        out_clk <= 0;
        count <= 0;
        temp_reg <= 1;
    end
    
    always @ (posedge clk)
    begin
        if (count == div_freq)
        begin
            count <= 0;
            out_clk <= ~out_clk;      
        end
        
        else
        begin
            count <= count + 1;
        end
    end
    
    always @(posedge clk)
    begin
        if (count == 0)
        begin
            temp_reg <= 1;
        end
        
        if (tx_complete == 1 && count>0)
        begin
            temp_reg <= 0;
        end
    end
    
    assign enable = temp_reg & out_clk;
     
endmodule  
''')

    # write the div_clk_temp
    with open(os.path.join(out_path, 'verilog_code', 'div_clk.v'), 'w') as f:
        f.write('''//// Clock Divider
module div_clk(clk, out);

    parameter div_freq = 0; // The frequency of clk = 125Mhz . Div_clk = 125Mhz/div_freq
    //We need 50KHz clock to get 50 KSPS from ADC sampling rate of ~960 KSPS
       
    input clk;
    output reg out;
    reg [31:0] count;
    
    initial
    begin
        out <= 0;
        count <= 0;
    end
    
    always @ (posedge clk)
    begin
        if (count == div_freq)
        begin
            out <= ~out;
            count <= 0; // Reset the counter
        end
        
        else
        begin
        count <= count + 1;
        end
    end
endmodule
''')

    sync_bits = "sync_bits"
    transmit_bits = "transmit_bits"

    # Create the TX module
    with open(os.path.join(out_path, 'verilog_code', 'tx.v'), 'w') as f:
        f.write(f'''//// Creating a transmission module
module tx(clk, enable, transmit_bits, tx_complete, out);

    input clk;  //clock frequency
    input enable;   //transmitter enable
    input [{n-1}:0]transmit_bits;   // Transmitter bits after CRC
    
    output reg tx_complete; // When tx_complete = 1 denote completion of frame transmission.
    output reg out;
    reg tx_state;   //State of transmitter FSM
    
    parameter tx_idle = 1'b0;
    parameter tx_tx = 1'b1;
    
    wire [7:0]sync_bits;  //Frame Synchronization bits
    reg [{n + 7}:0]tx_sr; //shift register for transmitting
    reg [{int(np.log2(n + 8))}:0]count;  //For keeping count of how many bits have been sent
    
    assign sync_bits[7:0] = 8'b10101010;  //Value of Sync bits
    
    initial
    begin
        tx_state <= tx_idle;
        count <= 0;
    end
    
    always @(posedge clk)
    begin
        if (enable & (~tx_state))   //Transmission enabled but Transmitter still in idle state
        begin
            tx_sr <= {sync_bits, transmit_bits};   //Put values in Shift register for transmittting     
            tx_state <= tx_tx;          //Change the state of transmitter FSM
            count <= 0;                //0 number of bits sent from current frame till now
            tx_complete <= 0;          // Set the tx_complete state to 0
        end
        
        if (tx_state==tx_tx)   //Transmitter is transmitting     
        begin
            out <= tx_sr[{n + 7}];     //Value of output sent to LED
            tx_sr[{n + 7}:1] <= tx_sr[{n + 6}:0];     //Output pin sends Most significant bit from Transmitter State Register
            tx_sr[0] <= 1'b0;
            count <= count+1;              //How many bits from shift register have been sent
        end
        
        if (count == {n + 8})        //All 32 bits transmitted
        begin
            tx_state <= tx_idle;    //Transmission complete hence FSM goes to idle state
            tx_complete <= 1;
        end
        
        if (tx_state == tx_idle)
        begin
            out <= 1'b0;
        end
    end
endmodule
''')

    # Writing Encoder module
    write_encoder_verilog(G_matrix, os.path.join(out_path, 'verilog_code', 'encoder.v'))


    # ADC Module
    with open(os.path.join(out_path, 'verilog_code', 'get_adc_data.v'), 'w') as f:
        f.write('''//Module for getting data from ADC
module get_adc_data(clk, v_n, v_p, data_out);
    input clk, v_n, v_p;
    output [11:0] data_out;
    reg [31:0] counter;
    
    wire [6:0] daddr_in = 7'h16;
    wire adc_ready, isbusy, adc_data_ready, eos_out, alarm;
    wire [15:0] adc_data;
    wire [4:0] channel_out;
    audio_adc XADC_INST (
        .daddr_in(7'h03),   // specifies vcaux6 pints to digitize
        .dclk_in(clk),    // 50MHz clock
        .den_in(adc_ready), // tied to adc_ready, tells adc to convert, tieing causes continuous conversions
        .di_in(16'h0),      // to set the data to something, not used here
        .dwe_in(1'b0),      //  set to enable writing to di_in, which we don't want to do
        .reset_in(1'b0),   //tells ADC to reset
        .busy_out(isbusy),  // tells you the adc is busy converting
        .channel_out(channel_out[4:0]), // for using more than 1 channel, tells you which one.  not used here
        .do_out(adc_data),      // adc value from conversion
        .drdy_out(adc_data_ready),  //tells you valid data is ready to be latched
        .eoc_out(adc_ready),   //  specifies that the ADC is ready (conversion complete)
        .eos_out(eos_out),     //  specifies that conversion sequence is complete
        .alarm_out(alarm),      // OR's output of all internal alarms, not used here
        .vp_in(v_p),           // dedicated analog input pair for differential, we are using this
        .vn_in(v_n)            // dedicated analog input pair for differential, we are using this
    );
    
    reg [15:0] ready_adc_data;
    always @ (posedge adc_data_ready) 
    begin
        ready_adc_data <= adc_data;
    end
    
    assign data_out = ready_adc_data[15:4];    
endmodule
''')

    # MAIN TRANSMITTER MODULE
    with open(os.path.join(out_path, 'verilog_code', 'transmitter.v'), 'w') as f:
        f.write(f"""module transmitter(main_clk, v_p, v_n, tx_out);
    input main_clk;
    input v_p, v_n;
    output tx_out;
    
    // Tx signal clock generator
    wire tx_clk;
    assign tx_clk = main_clk;
//    div_clk DC(main_clk, tx_clk);
    
    // Enable Control Unit
    wire adc_clk; // Clock at which the samples are updated
    wire tx_enable; // Enable bit for the tx
    wire tx_complete;      //Signal to determine transmission of frame completed
    Enable_Control_Unit ECU(main_clk, tx_complete, tx_enable, adc_clk);


    // Get data from the ADC
    wire [11:0] adc_data; //12-bit sampled audio output from ADC
    get_adc_data ADC(main_clk, v_n, v_p, adc_data);    //ADC data acquire module
    
    // Encoding the received frame
    reg [{k-1}:0] encoder_input; //Input to LDPC encoder 

    always @(posedge adc_clk)
    begin
        encoder_input[11:0] <= adc_data;
        encoder_input[{k-1}:{12}] <= {k-12}'b{''.join(['0' for _ in range(k-12)])}; 
    end
    
    wire [{n-1}:0] encoded_data;    //Data after being encoded
    encoder E(encoder_input, encoded_data);  //LDPC encoder module   
        
    // Transmitting the Encoded Frame   
    tx T(main_clk, tx_enable, encoded_data, tx_complete, tx_out);    //Transmitter module
    
endmodule
""")


    print("Verilog code generated successfully!")







