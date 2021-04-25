// Description of the LED panel:
// http://bikerglen.com/projects/lighting/led-panel-1up/#The_LED_Panel
//
// PANEL_[ABCD] ... select rows (in pairs from top and bottom half)
// PANEL_OE ....... display the selected rows (active low)
// PANEL_CLK ...... serial clock for color data
// PANEL_STB ...... latch shifted data (active high)
// PANEL_[RGB]0 ... color channel for top half
// PANEL_[RGB]1 ... color channel for bottom half
// taken from http://svn.clifford.at/handicraft/2015/c3demo/fpga/ledpanel.v
// modified by Niklas Fauth 2020

`default_nettype none
module ledpanel (
  input wire ctrl_clk,

	input wire ctrl_en,
	input wire [3:0] ctrl_wr,           // Which color memory block to write
	input wire [15:0] ctrl_addr,        // Addr to write color info on [col_info][row_info]
	input wire [23:0] ctrl_wdat,        // Data to be written [R][G][B]

	input wire display_clock,
	output reg panel_r0, panel_g0, panel_b0, panel_r1, panel_g1, panel_b1,
	output reg panel_clk, panel_stb, panel_oe
);

  parameter integer INPUT_DEPTH          = 6;    // bits of color before gamma correction
  parameter integer COLOR_DEPTH          = 7;    // bits of color after gamma correction
  parameter integer CHAINED              = 3; // number of panels in chain

  localparam integer SIZE_BITS = $clog2(CHAINED);

  reg [INPUT_DEPTH-1:0] video_mem_r [0:CHAINED*128-1];
	reg [INPUT_DEPTH-1:0] video_mem_g [0:CHAINED*128-1];
	reg [INPUT_DEPTH-1:0] video_mem_b [0:CHAINED*128-1];

  reg [COLOR_DEPTH-1:0] gamma_mem   [0:2**INPUT_DEPTH-1];

  initial begin:video_mem_init
		$readmemh("6bit_to_7bit_gamma.mem",gamma_mem);

        $readmemh("red.mem",video_mem_r);
        $readmemh("green.mem",video_mem_g);
        $readmemh("blue.mem",video_mem_b);
	end

  always @(posedge ctrl_clk) begin
		if (ctrl_en && ctrl_wr[2]) video_mem_r[ctrl_addr] <= ctrl_wdat[16+INPUT_DEPTH-1:16];
		if (ctrl_en && ctrl_wr[1]) video_mem_g[ctrl_addr] <= ctrl_wdat[8+INPUT_DEPTH-1:8];
		if (ctrl_en && ctrl_wr[0]) video_mem_b[ctrl_addr] <= ctrl_wdat[0+INPUT_DEPTH-1:0];
	end

	reg [7+COLOR_DEPTH+SIZE_BITS:0] cnt_x = 0;
	reg [2:0]                       cnt_z = 0;
	reg state = 0;

	reg [7+SIZE_BITS:0] addr_x;
	reg [2:0]           addr_z;
	reg [2:0]           data_rgb;
	reg [2:0]           data_rgb_q;
	reg [7+COLOR_DEPTH+SIZE_BITS:0] max_cnt_x;

	always @(posedge display_clock) begin
		case (cnt_z)
      0: max_cnt_x = 128*CHAINED+8;
      1: max_cnt_x = 256*CHAINED;
      2: max_cnt_x = 512*CHAINED;
      3: max_cnt_x = 1024*CHAINED;
      4: max_cnt_x = 2048*CHAINED;
      5: max_cnt_x = 4096*CHAINED;
      6: max_cnt_x = 8192*CHAINED;
      7: max_cnt_x = 16384*CHAINED;
		endcase
	end

	always @(posedge display_clock) begin
		state <= !state;
		if (!state) begin
			if (cnt_x > max_cnt_x) begin
				cnt_x <= 0;
				cnt_z <= cnt_z + 1;
				if (cnt_z == COLOR_DEPTH-1) begin
                    cnt_z <= 0;
                end
			end else begin
				cnt_x <= cnt_x + 1;
			end
		end
	end

	always @(posedge display_clock) begin
		panel_oe <= 128*CHAINED-8 < cnt_x && cnt_x < 128*CHAINED+8;
		if (state) begin
			panel_clk <= 1 < cnt_x && cnt_x < 128*CHAINED+2;
			panel_stb <= cnt_x == 128*CHAINED+2;
		end else begin
      panel_clk <= 0;
      panel_stb <= 0;
		end
	end

	always @(posedge display_clock) begin
		addr_x <= cnt_x[7+SIZE_BITS:0];
		addr_z <= cnt_z;
	end

	always @(posedge display_clock) begin
    data_rgb[2] <= gamma_mem[video_mem_r[addr_x]][addr_z];
    data_rgb[1] <= gamma_mem[video_mem_g[addr_x]][addr_z];
    data_rgb[0] <= gamma_mem[video_mem_b[addr_x]][addr_z];
	end

  always @(posedge display_clock) begin
		data_rgb_q <= data_rgb;
		if (!state) begin
			if (0 < cnt_x && cnt_x < 128*CHAINED+1) begin
				{panel_r1, panel_r0} <= {data_rgb[2], data_rgb_q[2]};
				{panel_g1, panel_g0} <= {data_rgb[1], data_rgb_q[1]};
				{panel_b1, panel_b0} <= {data_rgb[0], data_rgb_q[0]};
            end else begin
				{panel_r1, panel_r0} <= 0;
				{panel_g1, panel_g0} <= 0;
				{panel_b1, panel_b0} <= 0;
			end
		end
	end
endmodule
