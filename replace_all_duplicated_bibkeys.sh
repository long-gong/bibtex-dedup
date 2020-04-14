#!/usr/bin/env bash
set -e
tex_files=$(find ./ -type f | grep -E '\.tex')

for f in tex_files
do
    echo "Processing ${f} ..."
	echo "sed -i 's/Dai2017HighRadix/Dai2017HighRadixCrossbar/g' $f"
	sed -i 's/Dai2017HighRadix/Dai2017HighRadixCrossbar/g' $f
	echo "sed -i 's/Cakir2015HighRadix/Cakir_ModelingDesignHigh_2015/g' $f"
	sed -i 's/Cakir2015HighRadix/Cakir_ModelingDesignHigh_2015/g' $f
	echo "sed -i 's/Gong2017arXivSERENADE/GongLiuYangEtAl2018/g' $f"
	sed -i 's/Gong2017arXivSERENADE/GongLiuYangEtAl2018/g' $f
	echo "sed -i 's/GiacconePrabhakarShah2003SERENA/GiacconePrabhakarShah2003/g' $f"
	sed -i 's/GiacconePrabhakarShah2003SERENA/GiacconePrabhakarShah2003/g' $f
	echo "sed -i 's/GiacconePrabhakarShah2003SerenaJSAC/GiacconePrabhakarShah2003/g' $f"
	sed -i 's/GiacconePrabhakarShah2003SerenaJSAC/GiacconePrabhakarShah2003/g' $f
	echo "sed -i 's/McKeown_iLQF_1995/McKeown1995iLQF/g' $f"
	sed -i 's/McKeown_iLQF_1995/McKeown1995iLQF/g' $f
	echo "sed -i 's/ShahGiacconePrabhakar2002SerenaMicro/ShahGiacconePrabhakar2002serena/g' $f"
	sed -i 's/ShahGiacconePrabhakar2002SerenaMicro/ShahGiacconePrabhakar2002serena/g' $f
	echo "sed -i 's/Shah06MWM/ShahWischik2006MWM0/g' $f"
	sed -i 's/Shah06MWM/ShahWischik2006MWM0/g' $f
	echo "sed -i 's/Tassiulas1998TASS/Tassiulas1998/g' $f"
	sed -i 's/Tassiulas1998TASS/Tassiulas1998/g' $f
	echo "sed -i 's/ShahWischik2006MWM0/Shah06MWM/g' $f"
	sed -i 's/ShahWischik2006MWM0/Shah06MWM/g' $f
	echo "sed -i 's/Tassiulas90MaxWeight/Tassiulas90Max/g' $f"
	sed -i 's/Tassiulas90MaxWeight/Tassiulas90Max/g' $f
	echo "sed -i 's/Shah2012DelayBound/Shah2012queuescaling/g' $f"
	sed -i 's/Shah2012DelayBound/Shah2012queuescaling/g' $f
	echo "sed -i 's/Passas_CrossbarNoCsAre_2012/Passas2012bHighRadix/g' $f"
	sed -i 's/Passas_CrossbarNoCsAre_2012/Passas2012bHighRadix/g' $f
	echo "sed -i 's/cakir2016HighRadix/Cakir2016HighRadixCrossbar/g' $f"
	sed -i 's/cakir2016HighRadix/Cakir2016HighRadixCrossbar/g' $f
	echo "sed -i 's/GongTuneLiuEtAl2017QPS/Gong2017QPS/g' $f"
	sed -i 's/GongTuneLiuEtAl2017QPS/Gong2017QPS/g' $f
	echo "sed -i 's/GiacconePrabhakarShah2003/GiacconePrabhakarShah2003SERENA/g' $f"
	sed -i 's/GiacconePrabhakarShah2003/GiacconePrabhakarShah2003SERENA/g' $f
	echo "sed -i 's/GiacconePrabhakarShah2003SerenaJSAC/GiacconePrabhakarShah2003SERENA/g' $f"
	sed -i 's/GiacconePrabhakarShah2003SerenaJSAC/GiacconePrabhakarShah2003SERENA/g' $f
	echo "sed -i 's/Tamir_HighperformanceMulti_1988/Tamir1988VOQ/g' $f"
	sed -i 's/Tamir_HighperformanceMulti_1988/Tamir1988VOQ/g' $f
	echo "sed -i 's/Hu2018HRF/Hu_HighestRankFirst_2018/g' $f"
	sed -i 's/Hu2018HRF/Hu_HighestRankFirst_2018/g' $f
	echo "sed -i 's/LiPanwarChao2001DRRMProof/YihanLi_drr_2001/g' $f"
	sed -i 's/LiPanwarChao2001DRRMProof/YihanLi_drr_2001/g' $f
	echo "sed -i 's/Li2001DRR/YihanLi_drr_2001/g' $f"
	sed -i 's/Li2001DRR/YihanLi_drr_2001/g' $f
	echo "sed -i 's/McKeown1995iLQF/McKeown_iLQF_1995/g' $f"
	sed -i 's/McKeown1995iLQF/McKeown_iLQF_1995/g' $f
	echo "sed -i 's/ModianoShahZussman2006DistSched/ModianoShahZussman2006gossiping/g' $f"
	sed -i 's/ModianoShahZussman2006DistSched/ModianoShahZussman2006gossiping/g' $f
	echo "sed -i 's/Neely2007DelayBound/Neely2007FrameBased/g' $f"
	sed -i 's/Neely2007DelayBound/Neely2007FrameBased/g' $f
	echo "sed -i 's/Wang2016/Wang2016ParallelEdgeColoring/g' $f"
	sed -i 's/Wang2016/Wang2016ParallelEdgeColoring/g' $f
	echo "sed -i 's/GiacconePrabhakarShah2003/GiacconePrabhakarShah2003SerenaJSAC/g' $f"
	sed -i 's/GiacconePrabhakarShah2003/GiacconePrabhakarShah2003SerenaJSAC/g' $f
	echo "sed -i 's/GiacconePrabhakarShah2003SERENA/GiacconePrabhakarShah2003SerenaJSAC/g' $f"
	sed -i 's/GiacconePrabhakarShah2003SERENA/GiacconePrabhakarShah2003SerenaJSAC/g' $f
	echo "sed -i 's/Gong2017QPS/GongTuneLiuEtAl2017QPS/g' $f"
	sed -i 's/Gong2017QPS/GongTuneLiuEtAl2017QPS/g' $f
	echo "sed -i 's/Gupta2009DistributedMatching/Gupta2009DistSched/g' $f"
	sed -i 's/Gupta2009DistributedMatching/Gupta2009DistSched/g' $f
	echo "sed -i 's/Gupta_LowComplexityDistributed_2009/Gupta2009DistSched/g' $f"
	sed -i 's/Gupta_LowComplexityDistributed_2009/Gupta2009DistSched/g' $f
	echo "sed -i 's/ModianoShahZussman2006gossiping/ModianoShahZussman2006DistSched/g' $f"
	sed -i 's/ModianoShahZussman2006gossiping/ModianoShahZussman2006DistSched/g' $f
done