"""pdm 的行为测试台：开使能，写 data，读 mirror。

认矩阵：`dataWidth` 与 `invert` 都从这一点的旋钮来。占位符只在下面两个常量里出现，
不进 f-string——f-string 会把 {{ }} 当成自己的转义。
"""
import json
import pathlib
import sys

NAME = "pdm"
CAP = "Pdm"

out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
out.mkdir(parents=True, exist_ok=True)
cfg = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
label = cfg.get("label", "")
k = cfg.get("knobs", {})
w = int(k.get("dataWidth", 32))
invert = bool(k.get("invert", False))

mask = (1 << w) - 1
sent = 0xA5A5A5A5 & mask
want = (~sent & mask) if invert else sent

txt = f"""package {CAP}{label}Tb;

// 由 htest/mk{NAME}tb.py 生成，勿手改。这一点：dataWidth={w} invert={invert}

import StmtFSM::*;
import RegIf::*;
import {CAP}::*;

(* synthesize *)
module mk{CAP}{label}Tb(Empty);
  {CAP}Ifc#(8, 32, {w}) d <- mk{CAP}({CAP}Cfg {{ invert: {str(invert)} }});
  Reg#(Bool) bad <- mkReg(False);

  function Action wr(Bit#(8) a, Bit#(32) v) = action
    let x <- d.regs.access(RegReq {{ addr: a, write: True, wdata: v, wstrb: 4'hF }});
  endaction;

  function Action rd(Bit#(8) a, Bit#(32) exp, String what) = action
    let x <- d.regs.access(RegReq {{ addr: a, write: False, wdata: 0, wstrb: 4'hF }});
    if (x.rdata != exp || x.err) begin
      $display("FAIL %s reads %08h (err %0d), want %08h", what, x.rdata, x.err, exp);
      bad <= True;
    end
  endaction;

  Stmt test = seq
    wr(8'h04, 32'h{sent:08X});
    rd(8'h08, 32'h00000000, "mirror while disabled");
    wr(8'h00, 32'h00000001);
    rd(8'h08, 32'h{want:08X}, "mirror while enabled");
  endseq;

  FSM fsm <- mkFSM(test);
  Reg#(Bool) started <- mkReg(False);

  rule go (!started);
    started <= True;
    fsm.start;
  endrule

  rule fin (started && fsm.done);
    if (bad) $display("FAILED");
    else $display("PASS %s: mirror follows data only while enabled", "{NAME}");
    $finish(bad ? 1 : 0);
  endrule
endmodule

endpackage
"""

(out / f"{CAP}{label}Tb.bsv").write_text(txt, encoding="utf-8")
print(f"  {NAME} 行为测试台就位：dataWidth={w} invert={invert}")
