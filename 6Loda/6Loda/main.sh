#!/usr/bin/bash

# PWD: ipv6scan/
echo $SHELL
echo $PWD
# TODO: file path
foldername=6Loda
dataset=datasetTest

seeds_file_path=${foldername}/dataset/${dataset}/seeds.txt  # path of seed file
seeds_RFClabel_file_path=${foldername}/dataset/${dataset}/RFClabels.txt  # save path of seeds' RFC labels
ipv6_pred_save_path=${foldername}/result/${dataset}/pred.txt

ipv6_hit_icmp_save_path=${foldername}/result/cache/hit_icmp.txt        # save path of hit ip by zmap icmp test
ipv6_hit_tcp80_save_path=${foldername}/result/cache/hit_tcp80.txt      # save path of hit ip by zmap tcp80 test
ipv6_hit_tcp443_save_path=${foldername}/result/cache/hit_tcp443.txt    # save path of hit ip by zmap tcp443 test
ipv6_hit_udp80_save_path=${foldername}/result/cache/hit_udp80.txt      # save path of hit ip by zmap udp80 test
ipv6_hit_udp443_save_path=${foldername}/result/cache/hit_udp443.txt    # save path of hit ip by zmap udp443 test
ipv6_hit_save_path=${foldername}/result/${dataset}/hit.txt # save path of summarized results/all hit ip


# TODO: parameter setting
budget=35000
budget_testing_ratio=1

# TODO: tool path
ipv6toolkit_addr6_path=ipv6toolkit/addr6 


zmapTest(){
        # include ICMPv6, TCP/80, TCP/443, UDP/53, UDP/443
    sudo zmap \
        --ipv6-source-ip=2402:f000:4:1001:809:7403:1362:b5bd \
        --ipv6-target-file=$ipv6_pred_save_path \
        -M icmp6_echoscan \
        -B 10M \
        -o $ipv6_hit_icmp_save_path
    sudo zmap \
        --ipv6-source-ip=2402:f000:4:1001:809:7403:1362:b5bd \
        --ipv6-target-file=$ipv6_pred_save_path \
        -M tcp_synscan \
        -B 10M \
        -p 80 \
        -o $ipv6_hit_tcp80_save_path
    sudo zmap \
        --ipv6-source-ip=2402:f000:4:1001:809:7403:1362:b5bd \
        --ipv6-target-file=$ipv6_pred_save_path \
        -M tcp_synscan \
        -B 10M \
        -p 443 \
        -o $ipv6_hit_tcp443_save_path
    sudo zmap \
        --ipv6-source-ip=2402:f000:4:1001:809:7403:1362:b5bd \
        --ipv6-target-file=$ipv6_pred_save_path \
        -M udp \
        -B 10M \
        -p 80 \
        --probe-args=hex:02 \
        -o $ipv6_hit_udp80_save_path
    sudo zmap \
        --ipv6-source-ip=2402:f000:4:1001:809:7403:1362:b5bd \
        --ipv6-target-file=$ipv6_pred_save_path \
        -M udp \
        -B 10M \
        -p 443 \
        --probe-args=hex:02 \
        -o $ipv6_hit_udp443_save_path
    
    if [ -f $ipv6_hit_save_path ]; then
        rm $ipv6_hit_save_path
    fi
    cat $ipv6_hit_icmp_save_path   >> $ipv6_hit_save_path
    cat $ipv6_hit_tcp80_save_path  >> $ipv6_hit_save_path
    cat $ipv6_hit_tcp443_save_path >> $ipv6_hit_save_path
    cat $ipv6_hit_udp80_save_path  >> $ipv6_hit_save_path
    cat $ipv6_hit_udp443_save_path >> $ipv6_hit_save_path
}


# Identify the RFC category of seeds. Just execute once for one data set.
cat $seeds_file_path | $ipv6toolkit_addr6_path -i -d > $seeds_RFClabel_file_path


python ${foldername}/main.py \
    --seeds_RFClabel_file_path=$seeds_RFClabel_file_path \
    --seeds_file_path=$seeds_file_path \
    --ipv6_pred_save_path=$ipv6_pred_save_path \
    --budget=$budget \
    --budget_testing_ratio=$budget_testing_ratio \

zmapTest

echo "Successful execution!"