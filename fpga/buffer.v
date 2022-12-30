`default_nettype none
module udp_buffer(
    input clk,
    input rst,

    input  wire          udp_source_valid,
    input  wire          udp_source_last,
    input  wire  [15:0]  udp_source_dst_port,
    input  wire  [15:0]  udp_source_length,
    input  wire  [31:0]  udp_source_data,

    input wire udp_sink_ready,
    output wire udp_sink_valid,
    output wire udp_sink_last,
    output wire [15:0] udp_sink_dst_port,
    output wire [15:0] udp_sink_length,
    output wire [31:0] udp_sink_data
);

assign udp_sink_data[31:8] = 0; 
wire empty;

wire [40:0] dout;
wire [15:0] port;

assign port[7:0] = udp_source_dst_port[7:0];
assign port[15:8] = udp_source_dst_port[15:8] - 1;

assign {udp_sink_length, udp_sink_dst_port, udp_sink_last, udp_sink_data[7:0]} = udp_sink_valid ? dout : 0;

assign udp_sink_valid = ~empty;

fifo_fwft
    #(.DEPTH_WIDTH (10),
      .DATA_WIDTH (40))
fifo0
    (
        .clk(clk),
        .rst(rst),
        .din({udp_source_length, port, udp_source_last, udp_source_data[7:0]}),
        .wr_en(udp_source_valid),
        .full(),
        .dout(dout),
        .rd_en(udp_sink_ready),
        .empty(empty));

endmodule