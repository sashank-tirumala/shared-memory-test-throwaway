#!/bin/bash

# Function to create a new tmux pane and run a command
create_pane() {
    tmux split-window -t stress_test
    tmux send-keys -t stress_test "$1; read -p 'Press Enter to close this pane...'" C-m
    tmux select-layout tiled
}

# Create a new tmux session named stress_test
tmux new-session -d -s stress_test

# Start the writer
tmux send-keys -t stress_test "python writer.py; read -p 'Press Enter to close this pane...'" C-m

# Wait for a second
sleep 1

# Create 10 readers
for i in {1..10}
do
    create_pane "python reader.py --reader $i"
done

# Attach to the tmux session
tmux attach-session -t stress_test