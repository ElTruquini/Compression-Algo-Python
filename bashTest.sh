#!/bin/bash  

echo "Initializing: Testing scrypt for assignment 2"  

var_t=t
var_zero=0
var_extf=.txt
var_extb=.ph1

var_namef=''
var_nameb=''
var_bs=''

var_resultb=()
var_resultf=()

for i in {1..20}
	do
		echo "***************************************"
		if (($i < 10)) ; then
			var_nameb="$var_t$var_zero$i$var_extb"
			var_namef="$var_t$var_zero$i$var_extf"
			var_bs=20

		fi

		if (($i < 12)) && (( $i >= 10 )) ; then
			var_nameb="$var_t$i$var_extb"
			var_namef="$var_t$i$var_extf"
			var_bs=20

		fi

		if (($i == 12)) ; then
			var_nameb="$var_t$i$var_extb"
			var_namef="$var_t$i$var_extf"
			var_bs=50

		fi

		if (($i == 13)) ; then
			var_nameb="$var_t$i$var_extb"
			var_namef="$var_t$i$var_extf"
			var_bs=100

		fi

		if (($i == 14)) ; then
			var_nameb="$var_t$i$var_extb"
			var_namef="$var_t$i$var_extf"
			var_bs=200	
		fi

		if (($i == 15)) ; then
			var_nameb="$var_t$i$var_extb"
			var_namef="$var_t$i$var_extf"
			var_bs=500
		
		fi

		if (($i == 16)) ; then
			var_nameb="$var_t$i$var_extb"
			var_namef="$var_t$i$var_extf"
			var_bs=20
		fi

		if (($i == 17)) ; then
			var_nameb="$var_t$i$var_extb"
			var_namef="$var_t$i$var_extf"
			var_bs=50
		fi

		if (($i == 18)) ; then
			var_nameb="$var_t$i$var_extb"
			var_namef="$var_t$i$var_extf"
			var_bs=100
		fi

		if (($i == 19)) ; then
			var_nameb="$var_t$i$var_extb"
			var_namef="$var_t$i$var_extf"
			var_bs=200
		fi

		if (($i == 20)) ; then
			var_nameb="$var_t$i$var_extb"
			var_namef="$var_t$i$var_extf"
			var_bs=500


		fi


		./phase1.py --backward --infile ./tests/$var_nameb --outfile a.txt --blocksize $var_bs
		if diff a.txt ./tests/$var_namef >/dev/null ; then
		  echo "RESULT: PASS Test $i backward - Files are equal"
		  var_resultb[$i]=1
		
		else 
		  echo "RESULT: FAIL Test $i backward - Files differ*"
		  var_resultb[$0]=0
		fi

		./phase1.py --forward --infile ./tests/$var_namef --outfile a.txt --blocksize $var_bs
		if diff a.txt ./tests/$var_nameb >/dev/null ; then
		  echo "PASS Test $i backward - Files are equal"
		  var_resultf[$i]=1
		
		else 
		  echo "FAIL Test $i backward - Files differ*"
		  var_resultf[$i]=0
		fi
done

for i in {1..20}
	do
		if ((${var_resultf[$i]} == 1)) ; then
		    echo "TEST FORWARD: $i - PASS"
		else
			echo "TEST FORWARD: $i - FAILED*"
		fi
done

for i in {1..20}
	do
		if ((${var_resultb[$i]} == 1)) ; then
			echo "TEST BACKWARD: $i - PASS"
		else
			echo "TEST BACKWARD: $i - FAILED*"
		fi
done


exit 1