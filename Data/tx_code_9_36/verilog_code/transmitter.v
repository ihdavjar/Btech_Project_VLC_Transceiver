//////// TMDS - {TMDS_Clk_p, TMDS_Clk_n, TMDS_Data_p[2:0], TMDS_Data_n[2:0]} 

// Module to generate PWM output
module gen_pwm(clk, data_in, data_out);
    input clk; // Clock input f = 2^11*1KHz ~ 2MHz
    input [11:0] data_in; // 11 bit data input
    reg [11:0] temp_data;
    output data_out; // Output PWM data
    
    reg [8:0] counter;
    
    initial
    begin
        counter <= 0;
    end
    
    always @(posedge clk)
    begin
        if (counter == 2048)
        begin
            temp_data <= data_in;
            counter <= 0;
        end
        else
        begin
            counter <= counter+1;
        end
    end
    
    assign data_out = (counter < temp_data);
 endmodule
 
module transmitter(main_clk, TMDS, tx_out, pwm_out);
    input main_clk;
    input [7:0] TMDS;
    output tx_out, pwm_out;
    
    // Tx signal clock generator
    wire tx_clk;
    assign tx_clk = main_clk;
//    div_clk DC(main_clk, tx_clk);
    
    // Enable Control Unit
    wire pixel_clk; // Clock at which the pixels are generated.
    wire tx_enable; // Enable bit for the tx
    wire tx_complete; //Signal to determine transmission of frame completed
    Enable_Control_Unit ECU(main_clk, tx_complete, tx_enable, pixel_clk);


    // Get data from the ADC
    wire [26:0] pixel_data; //12-bit sampled audio output from ADC
    get_pixel_data pix(main_clk, TMDS, pixel_data);    //ADC data acquire module
    
    // Encoding the received frame
    reg [26:0] encoder_input; //Input to LDPC encoder 
    reg [10:0] pwm_in;

    always @(posedge pixel_clk)
    begin
        encoder_input <= pixel_data;
        pwm_in <= pixel_data[10:0]; 
    end
    
    wire [35:0] encoded_data;    //Data after being encoded
    encoder E(encoder_input, encoded_data);  //LDPC encoder module   
    
    
    
        
    // Transmitting the Encoded Frame   
    tx T(tx_clk, tx_enable, encoded_data, tx_complete, tx_out);    //Transmitter module
    
    gen_pwm PWM(main_clk, pwm_in, pwm_out);
    
endmodule
