from collections import defaultdict, Counter


def player(prev_play, state={}):
    beats = {
        "R": "P",
        "P": "S",
        "S": "R"
    }

    moves = ["R", "P", "S"]

    # Reset the player's memory at the beginning of each new match.
    if not state or prev_play == "":
        state.clear()
        state["opponent_history"] = []
        state["my_history"] = []
        state["last_predictions"] = {}
        state["scores"] = defaultdict(float)

    opponent_history = state["opponent_history"]
    my_history = state["my_history"]

    # After the first round, prev_play is the opponent's last move.
    # Use it to score how accurate each predictor was.
    if prev_play:
        opponent_history.append(prev_play)

        for predictor_name, prediction in state["last_predictions"].items():
            if prediction == prev_play:
                state["scores"][predictor_name] += 1
            else:
                state["scores"][predictor_name] -= 0.25

    predictions = {}

    # Predictor for Kris:
    # Kris plays the move that beats our previous move.
    predictions["kris"] = beats[my_history[-1]] if my_history else "R"

    # Predictor for Mrugesh:
    # Mrugesh looks at the most frequent move from our last 10 moves
    # and plays the move that beats it.
    mrugesh_history = ([""] + my_history)[-10:]
    most_frequent = max(set(mrugesh_history), key=mrugesh_history.count)

    if most_frequent == "":
        most_frequent = "S"

    predictions["mrugesh"] = beats[most_frequent]

    # Predictor for Abbey:
    # Abbey tracks pairs of our moves and predicts our next move based on
    # the most common pair that begins with our previous move.
    play_order = {
        first + second: 0
        for first in moves
        for second in moves
    }

    simulated_history = []

    for move in ["R"] + my_history:
        simulated_history.append(move)
        last_two = "".join(simulated_history[-2:])

        if len(last_two) == 2 and last_two in play_order:
            play_order[last_two] += 1

    previous_my_move = my_history[-1] if my_history else "R"
    possible_pairs = [
        previous_my_move + "R",
        previous_my_move + "P",
        previous_my_move + "S"
    ]

    sub_order = {
        pair: play_order[pair]
        for pair in possible_pairs
    }

    predicted_my_next_move = max(sub_order, key=sub_order.get)[-1]
    predictions["abbey"] = beats[predicted_my_next_move]

    # Predictor for Quincy:
    # Quincy follows a five-step cycle. Since the same value appears twice,
    # using the move from four turns ago predicts the next move well.
    predictions["quincy"] = (
        opponent_history[-4]
        if len(opponent_history) >= 4
        else "R"
    )

    # Generic Markov predictors based on the opponent's own history.
    for n in range(1, 6):
        if len(opponent_history) > n:
            pattern = "".join(opponent_history[-n:])
            counts = Counter()

            for index in range(len(opponent_history) - n):
                if "".join(opponent_history[index:index + n]) == pattern:
                    counts[opponent_history[index + n]] += 1

            if counts:
                predictions[f"opponent_markov_{n}"] = counts.most_common(1)[0][0]

    # Generic Markov predictors based on our move history.
    # This helps against bots that react to what we played.
    for n in range(1, 6):
        if len(my_history) >= n and len(opponent_history) >= n:
            pattern = "".join(my_history[-n:])
            counts = Counter()

            for index in range(n, len(my_history)):
                if "".join(my_history[index - n:index]) == pattern:
                    counts[opponent_history[index]] += 1

            if counts:
                predictions[f"my_markov_{n}"] = counts.most_common(1)[0][0]

    # Choose the predictor that has been most accurate so far.
    best_predictor = max(
        predictions.keys(),
        key=lambda name: state["scores"].get(name, 0)
    )

    predicted_opponent_move = predictions[best_predictor]

    # Play the move that beats the predicted opponent move.
    guess = beats[predicted_opponent_move]

    my_history.append(guess)
    state["last_predictions"] = predictions

    return guess
