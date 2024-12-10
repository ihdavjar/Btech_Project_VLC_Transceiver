module encoder(frame_data, out);
    input [26:0] frame_data; // Frame bits
    output [35:0] out; // Output encoded bits with parity bits = 36


    assign out[9] = frame_data[0];
    assign out[10] = frame_data[1];
    assign out[11] = frame_data[2];
    assign out[12] = frame_data[3];
    assign out[13] = frame_data[4];
    assign out[14] = frame_data[5];
    assign out[15] = frame_data[6];
    assign out[16] = frame_data[7];
    assign out[17] = frame_data[8];
    assign out[18] = frame_data[9];
    assign out[19] = frame_data[10];
    assign out[20] = frame_data[11];
    assign out[21] = frame_data[12];
    assign out[22] = frame_data[13];
    assign out[23] = frame_data[14];
    assign out[24] = frame_data[15];
    assign out[25] = frame_data[16];
    assign out[26] = frame_data[17];
    assign out[27] = frame_data[18];
    assign out[28] = frame_data[19];
    assign out[29] = frame_data[20];
    assign out[30] = frame_data[21];
    assign out[31] = frame_data[22];
    assign out[32] = frame_data[23];
    assign out[33] = frame_data[24];
    assign out[34] = frame_data[25];
    assign out[35] = frame_data[26];


    assign out[0] = frame_data[0] ^ frame_data[1] ^ frame_data[4] ^ frame_data[5] ^ frame_data[6] ^ frame_data[7] ^ frame_data[8] ^ frame_data[9] ^ frame_data[12] ^ frame_data[14] ^ frame_data[16] ^ frame_data[17] ^ frame_data[18] ^ frame_data[19] ^ frame_data[23] ^ frame_data[25];
    assign out[1] = frame_data[0] ^ frame_data[2] ^ frame_data[3] ^ frame_data[4] ^ frame_data[5] ^ frame_data[8] ^ frame_data[13] ^ frame_data[14] ^ frame_data[18] ^ frame_data[19] ^ frame_data[20] ^ frame_data[21] ^ frame_data[25] ^ frame_data[26];
    assign out[2] = frame_data[0] ^ frame_data[4] ^ frame_data[6] ^ frame_data[8] ^ frame_data[9] ^ frame_data[14] ^ frame_data[15] ^ frame_data[20] ^ frame_data[21] ^ frame_data[23] ^ frame_data[24] ^ frame_data[25] ^ frame_data[26];
    assign out[3] = frame_data[0] ^ frame_data[1] ^ frame_data[2] ^ frame_data[3] ^ frame_data[7] ^ frame_data[10] ^ frame_data[11] ^ frame_data[12] ^ frame_data[13] ^ frame_data[14] ^ frame_data[16] ^ frame_data[17] ^ frame_data[18] ^ frame_data[21] ^ frame_data[22] ^ frame_data[25] ^ frame_data[26];
    assign out[4] = frame_data[1] ^ frame_data[2] ^ frame_data[5] ^ frame_data[13] ^ frame_data[15] ^ frame_data[17] ^ frame_data[22] ^ frame_data[23] ^ frame_data[24] ^ frame_data[25] ^ frame_data[26];
    assign out[5] = frame_data[0] ^ frame_data[1] ^ frame_data[5] ^ frame_data[7] ^ frame_data[8] ^ frame_data[9] ^ frame_data[11] ^ frame_data[12] ^ frame_data[13] ^ frame_data[14] ^ frame_data[15] ^ frame_data[17] ^ frame_data[18] ^ frame_data[19] ^ frame_data[20] ^ frame_data[21] ^ frame_data[24] ^ frame_data[26];
    assign out[6] = frame_data[1] ^ frame_data[5] ^ frame_data[7] ^ frame_data[8] ^ frame_data[11] ^ frame_data[12] ^ frame_data[14] ^ frame_data[15] ^ frame_data[19] ^ frame_data[21] ^ frame_data[22] ^ frame_data[24] ^ frame_data[25] ^ frame_data[26];
    assign out[7] = frame_data[5] ^ frame_data[6] ^ frame_data[8] ^ frame_data[9] ^ frame_data[12] ^ frame_data[15] ^ frame_data[16] ^ frame_data[23] ^ frame_data[26];
    assign out[8] = frame_data[0] ^ frame_data[1] ^ frame_data[3] ^ frame_data[4] ^ frame_data[5] ^ frame_data[8] ^ frame_data[9] ^ frame_data[12] ^ frame_data[14] ^ frame_data[15] ^ frame_data[16] ^ frame_data[17] ^ frame_data[20] ^ frame_data[21] ^ frame_data[22] ^ frame_data[23];

endmodule
