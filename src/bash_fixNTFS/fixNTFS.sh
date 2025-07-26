#!/usr/bin/env bash
function findvol(){
		lsblk --list -o FSTYPE,PATH | awk '$1 == "ntfs" {print $2}'|xargs -n 1 printf  '%s ' 
}
function countvol(){
		vol=$1
		echo "${#vol[@]}"
}
function pfixvol(){
		CNT=$1
		VOL=$(echo -e $2)
		CUR=0
		printf '%s/%s  ' CUR=$((CUR+1)) $CNT
		printf '%s'  $VOL

		echo -e $VOL | parallel --max-args=1 --jobs=$CNT ntfsfix #&> ntFixFS.fix.log
		echo -e 'FIXED'
		echo -e $VOL | parallel --max-args=1 --jobs=$CNT ntfsfix -d # &>ntfixfs.dirty.log
		echo -e 'CLEARED'
		echo -e '\n'
}
VOL=($(findvol))
CNT="${#VOL[@]}"
for i in "${VOL[@]}"; do
	pfixvol $CNT  $i
done

echo done

function fixNTFS(){

	FNC=${FUNCNAME[0]}
	case "$1" in
		p)     pfixvol  &>/dev/null;;
		s)     sfixvol  2>/dev/null;;
		debug)     shift && set -o xtrace && $FNC $@;;
		*)         pfixVol
	esac

}
