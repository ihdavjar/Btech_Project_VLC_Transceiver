//// Creating a transmission module
module tx(clk, enable, transmit_bits, tx_complete, out);

    input clk;  //clock frequency
    input enable;   //transmitter enable
    input [35:0]transmit_bits;   // Transmitter bits after CRC
    
    output reg tx_complete; // When tx_complete = 1 denote completion of frame transmission.
    output reg out;
    reg tx_state;   //State of transmitter FSM
    
    parameter tx_idle = 1'b0;
    parameter tx_tx = 1'b1;
    
    wire [7:0]sync_bits;  //Frame Synchronization bits
    reg [43:0]tx_sr; //shift register for transmitting
    reg [5:0]count;  //For keeping count of how many bits have been sent
    
    assign sync_bits[7:0] = 8'b10101010;  //Value of Sync bits
    
    initial
    begin
        tx_state <= tx_idle;
        count <= 0;
        tx_complete <= 1;
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
            out <= tx_sr[43];     //Value of output sent to LED
            tx_sr[43:1] <= tx_sr[42:0];     //Output pin sends Most significant bit from Transmitter State Register
            tx_sr[0] <= 1'b0;
            count <= count+1;              //How many bits from shift register have been sent
        end
        
        if (count == 44)        //All 32 bits transmitted
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
