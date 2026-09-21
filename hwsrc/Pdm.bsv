package Pdm;

import RegIf::*;
import PdmRegs::*;

typedef struct {
  Bool invert;
} PdmCfg;

interface PdmIfc#(numeric type aw, numeric type dw, numeric type dataWidth);
  interface RegIf#(aw, dw) regs;
endinterface

// 每种不同的字段宽度各要一条 Add#(_, 宽, dw)：生成的寄存器组把字段零扩展到 dw，
// 那条 proviso 由调用方带上。这里是 1 位的 ctrl.enable 与 dataWidth 位的 data。
module mkPdm#(PdmCfg cfg)(PdmIfc#(aw, dw, dataWidth))
    provisos (Mul#(TDiv#(dw, 8), 8, dw), Add#(_a, 8, aw),
              Add#(_b, dataWidth, dw), Add#(_c, 1, dw));

  PdmRegsIfc#(aw, dw, dataWidth) r <- mkPdmRegs;

  rule drive;
    Bool on = unpack(r.ctrl_enable);
    Bit#(dataWidth) v = cfg.invert ? ~r.data : r.data;
    r.mirror_in(on ? v : 0);
  endrule

  interface regs = r.regs;
endmodule

endpackage
