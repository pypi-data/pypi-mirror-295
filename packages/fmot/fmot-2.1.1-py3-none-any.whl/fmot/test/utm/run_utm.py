from fmot import CONFIG
from fmot.test.utm.get_utms import ALL_UTMS
import argparse
import torch
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--testcase", type=str, choices=ALL_UTMS.keys())
parser.add_argument("--precision", type=str, default="double")
parser.add_argument("--rounded", type=bool, default=False)
args = parser.parse_args()


utm = ALL_UTMS[args.testcase]
print(utm)

input = utm.get_random_inputs(batch_size=1)
print([x.shape for x in input])
input_np = [x.numpy()[0] for x in input]
qmodel = utm.get_quantized_model(bw_conf=args.precision)
graph = utm.get_fqir(bw_conf=args.precision)

with torch.no_grad():
    y0 = qmodel(*input)
y1 = graph.run(*input_np, dequant=True)

if isinstance(y0, (list, tuple)):
    y0 = y0[0]
    y1 = y1[0]
y0 = y0[0].numpy()

# plt.plot(y0.flatten(), y1.flatten(), '.')
# plt.show()

utm.test_fqir_runtime(bw_conf=args.precision)


CONFIG.quant_round = args.rounded
graph = utm.get_fqir(bw_conf=args.precision)
print(graph.subgraphs["ARITH"])
utm.test_fqir_runtime(bw_conf=args.precision)
