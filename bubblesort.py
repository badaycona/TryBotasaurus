prices = [1200, 800, 1500, 950, 1100, 600]
print(prices)
for i in range(len(prices)):
    for j in range(i + 1, len(prices)):
        if prices[j] < prices[i] : 
            prices[i], prices[j] = prices[j], prices[i]
        
print(prices)