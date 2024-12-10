//Module for getting data from ADC
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
