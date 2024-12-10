//// Clock Divider
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
