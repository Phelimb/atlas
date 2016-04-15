import sys
from mykatlas.cortex import McCortexJoin
from mykatlas.cortex.mccortex import McCortexSubgraph
from mykatlas.cortex.mccortex import McCortexUnitigs


def run(parser, args):
    assert args.ctx
    # Build the intersection
    mccortex_join = McCortexJoin(
        sample=args.sample,
        intersect_graph=args.graph,
        ingraph=args.ctx)
    intersect_graph_out_path = mccortex_join.run()
    # Remove the intersection from the original graph
    mccortex_subgraph = McCortexSubgraph(
        sample=args.sample,
        rmgraph=intersect_graph_out_path,
        ingraph=args.ctx,
        tmp_dir=mccortex_join.out_ctx_dir)
    new_graph_out_path = mccortex_subgraph.run()
    # Output unitigs
    mccortex_unitigs = McCortexUnitigs(ingraph=new_graph_out_path)
    sys.stdout.write(mccortex_unitigs.run())
