n = int(input())
scores = list(map(int, input().split()))

# Encontrar o maior score
max_score = max(scores)

# Encontrar o segundo maior score (runner-up)
runner_up = None
for score in scores:
    if score != max_score and (runner_up is None or score > runner_up):
        runner_up = score

print(runner_up)
