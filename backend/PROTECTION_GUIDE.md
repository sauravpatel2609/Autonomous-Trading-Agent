# 🛡️ AUTOMATIC STOCK PROTECTION GUIDE

## When You Stop the Trading Agent

### ⚡ IMMEDIATE PROTECTION (Automatic)
When you press **Ctrl+C** to stop the agent, it will automatically:
1. 🛑 Detect the shutdown signal
2. 📊 Check your current positions  
3. 🛡️ Place a **3% stop-loss order** automatically
4. ✅ Your position is protected even when agent is offline!

### 🔧 MANUAL PROTECTION (Advanced)
If you want custom protection, run the stop-loss manager:

```bash
cd c:/Users/saura/OneDrive/Desktop/project/backend
python -m src.stop_loss_manager
```

## 📋 Protection Options:

### 1️⃣ **Stop-Loss Order** (Prevents Big Losses)
- **What**: Automatically sells if price drops X%
- **Example**: Stock at $100, 5% stop-loss = sells at $95
- **Good for**: Protecting against major drops

### 2️⃣ **Take-Profit Order** (Locks in Gains)  
- **What**: Automatically sells if price rises X%
- **Example**: Stock at $100, 10% take-profit = sells at $110
- **Good for**: Securing profits when target reached

### 3️⃣ **Both Orders** (Complete Protection)
- **What**: Combines stop-loss + take-profit
- **Good for**: Full automation - protects losses AND locks gains

### 4️⃣ **Emergency Sell** (Immediate Exit)
- **What**: Sells ALL shares RIGHT NOW at market price
- **Good for**: When you want out immediately

## 🚨 IMPORTANT NOTES:

✅ **Orders work 24/7** - Even when your computer is off!  
✅ **Broker executes** - Alpaca handles it, not your agent  
✅ **GTC Orders** - "Good Till Cancelled" means they stay active until executed  
✅ **Paper Trading** - Safe to test with fake money first  

## 🔄 WORKFLOW EXAMPLE:

1. **Start Agent**: `python -m src.agent --ticker AAPL`
2. **Agent Buys**: Automatically buys AAPL when AI predicts up
3. **Stop Agent**: Press Ctrl+C when you want to stop
4. **Auto-Protection**: Agent places 3% stop-loss automatically
5. **Protected**: Your AAPL position is now protected even offline!

## 💡 PRO TIPS:

- **Use 3-5% stop-loss** for aggressive protection
- **Use 8-15% take-profit** for reasonable targets  
- **Check orders** in your Alpaca account to see active protection
- **Cancel orders** using option 5 if you change your mind

## 🆘 EMERGENCY COMMANDS:

**Stop agent + protect position:**
```bash
# Press Ctrl+C (agent auto-protects)
```

**Manual emergency sell everything:**
```bash
python -m src.stop_loss_manager
# Choose option 4: Emergency sell ALL shares
```

**Cancel all protection orders:**
```bash
python -m src.stop_loss_manager  
# Choose option 5: Cancel all orders
```

Your stocks are now protected! 🛡️
