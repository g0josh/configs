usage=`top -bn2 -d0.1 |grep 'load average'|tail -n1|awk '{print $10}'|cut -c -4`
cores=`cat /proc/cpuinfo|grep 'cpu cores'|tail -n1|awk '{print $4}'`
cpuusage=$(echo "${usage}*100/${cores}"|bc)
gpuusage=`nvidia-smi -q -d UTILIZATION|grep Gpu|awk '{print $3}'`
echo "${cpuusage}|${gpuusage}"
