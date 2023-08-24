#!/bin/bash

# don't contain spaces in SESSION name for convenience.
SESSION="test"
SESSIONEXISTS=$(tmux list-sessions | grep $SESSION)

COMMANDS=(
	"0 CDS_QPLEX benchmark_academy_3_vs_1_with_keeper"
    "0 CDS_QPLEX benchmark_academy_corner"
    "0 CDS_QPLEX benchmark_academy_counterattack_easy"
    "1 CDS_QPLEX benchmark_academy_counterattack_hard"
    "1 CDS_QPLEX benchmark_academy_pass_and_shoot_with_keeper"
    "1 CDS_QPLEX benchmark_academy_run_pass_and_shoot_with_keeper"
    "2 CDS_QPLEX benchmark_academy_3_vs_1_with_keeper"
    "2 CDS_QPLEX benchmark_academy_corner"
    "2 CDS_QPLEX benchmark_academy_counterattack_easy"
    "3 CDS_QPLEX benchmark_academy_counterattack_hard"
    "3 CDS_QPLEX benchmark_academy_pass_and_shoot_with_keeper"
    "3 CDS_QPLEX benchmark_academy_run_pass_and_shoot_with_keeper"
    "4 CDS_QPLEX benchmark_academy_3_vs_1_with_keeper"
    "4 CDS_QPLEX benchmark_academy_corner"
    "4 CDS_QPLEX benchmark_academy_counterattack_easy"
    "5 CDS_QPLEX benchmark_academy_counterattack_hard"
    "5 CDS_QPLEX benchmark_academy_pass_and_shoot_with_keeper"
    "5 CDS_QPLEX benchmark_academy_run_pass_and_shoot_with_keeper"
    "6 CDS_QPLEX benchmark_academy_3_vs_1_with_keeper"
    "6 CDS_QPLEX benchmark_academy_corner"
    "6 CDS_QPLEX benchmark_academy_counterattack_easy"
    "7 CDS_QPLEX benchmark_academy_counterattack_hard"
    "7 CDS_QPLEX benchmark_academy_pass_and_shoot_with_keeper"
    "7 CDS_QPLEX benchmark_academy_run_pass_and_shoot_with_keeper"
    # "0 CDS_QPLEX benchmark_full_game_5_vs_5_hard"
    # "0 CDS_QPLEX benchmark_full_game_11_vs_11_hard"
    # "1 CDS_QPLEX benchmark_full_game_5_vs_5_hard"
    # "1 CDS_QPLEX benchmark_full_game_11_vs_11_hard"
    # "2 CDS_QPLEX benchmark_full_game_5_vs_5_hard"
    # "2 CDS_QPLEX benchmark_full_game_11_vs_11_hard"
    # "3 CDS_QPLEX benchmark_full_game_5_vs_5_hard"
    # "3 CDS_QPLEX benchmark_full_game_11_vs_11_hard"
    # "4 CDS_QPLEX benchmark_full_game_5_vs_5_hard"
    # "4 CDS_QPLEX benchmark_full_game_11_vs_11_hard"
    # "5 CDS_QPLEX benchmark_full_game_5_vs_5_hard"
    # "5 CDS_QPLEX benchmark_full_game_11_vs_11_hard"
    # "6 CDS_QPLEX benchmark_full_game_5_vs_5_hard"
    # "6 CDS_QPLEX benchmark_full_game_11_vs_11_hard"
    # "7 CDS_QPLEX benchmark_full_game_5_vs_5_hard"
    # "7 CDS_QPLEX benchmark_full_game_11_vs_11_hard"
)

if [[ -z "${SESSIONEXISTS}" ]]
then
	echo "build the session ${SESSION}"
	for ((i = 0; i < ${#COMMANDS[@]}; i++))
	do
		WINDOW_IDX=$i
		COMMAND=${COMMANDS[$i]}
        DEVICE=$(echo $COMMAND | cut -d " " -f 1)
        ALGO=$(echo $COMMAND | cut -d " " -f 2)
        ENV=$(echo $COMMAND | cut -d " " -f 3)
        RUN_COMMAND="CUDA_VISIBLE_DEVICES=$DEVICE python main.py --config=$ALGO --env-config=$ENV"
		WINDOW_NAME="${ENV}_${DEVICE}"
		echo send keys to window $WINDOW_NAME: $RUN_COMMAND
		if [[ $i == 0 ]]
		then 
			tmux new-session -d -s $SESSION
			tmux rename-window -t $SESSION:$WINDOW_IDX "$WINDOW_NAME"
			tmux send-keys -t $SESSION:$WINDOW_IDX "$RUN_COMMAND" Enter
		else
			tmux new-window -t $SESSION:$WINDOW_IDX -n "$WINDOW_NAME"
			tmux send-keys -t $SESSION:$WINDOW_IDX "$RUN_COMMAND" Enter
		fi
	done
	# tmux new-session -d -s $SESSION
	# window=0
	# tmux rename-window -t $SESSION:$WINDOW 'git'
	# tmux send-keys -t $SESSION:$WINDOW 'git --version' Enter
else
	echo "please enter \"tmux attach -t $SESSION\" to attach the session."
fi
