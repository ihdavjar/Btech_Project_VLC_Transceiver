//// Control Unit for Enable
module Enable_Control_Unit(clk, tx_complete, enable, out_clk);

    parameter div_freq = 25; // Freq = 12.5MHz/div_freq (According to the sampling frequency)
    
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
