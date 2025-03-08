<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dexscreener Bot Setup</title>
    <style>
        body {
            background-color: #121212;
            color: #e0e0e0;
            font-family: Arial, sans-serif;
        }

        .filters-container {
            font-family: Arial, sans-serif;
            padding: 15px;
            border: 1px solid #555;
            border-radius: 8px;
            max-width: 350px;
            background: #333;
            margin-top: 20px;
        }

        .filter-group {
            margin: 15px 0;
        }

        .filter-label {
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
        }

        .input-row {
            display: flex;
            gap: 10px;
        }

        .input-wrapper {
            display: flex;
            align-items: center;
            border: 1px solid #555;
            padding: 5px;
            border-radius: 5px;
            width: 100%;
            background: #444;
        }

        .input-prefix, .input-suffix {
            padding: 0 5px;
            font-weight: bold;
        }

        input {
            border: none;
            outline: none;
            flex-grow: 1;
            background: transparent;
            text-align: left;
            color: #e0e0e0;
        }

        select {
            border: 1px solid #555;
            padding: 5px;
            border-radius: 5px;
            background: #444;
            color: #e0e0e0;
            width: 100%;
        }

        button {
            cursor: pointer;
        }

        #filterPopup {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #222;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.7);
            z-index: 1000;
            width: 400px;
        }

        #filterPopup h2 {
            margin: 0 0 15px;
            text-align: center;
            color: #64b5f6;
        }

        .error {
            border: 2px solid #ff5722;
        }

        /* Modal overlay to darken the background when popup is open */
        #modalOverlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
            z-index: 900;
        }
    </style>
</head>
<body>
    <h1>Hello User! 👋</h1>
    <p>This will scrape from Dexscreener trending tokens by running the <a href="/dex" style="color: #64b5f6; text-decoration: underline;">/dex</a> path.</p>
    <ol>
        <li>You need to add a bot inside a group. 🤖</li>
        <li>You need to get the channel ID. 📨</li>
        <li>You need to get the WebSocket URL for the filters for the Dexscreener. Use this format:
            <pre style="background-color: #333; padding: 10px;">wss://io.dexscreener.com/dex/screener/v4/pairs/h24/1?rankBy[key]=trendingScoreH6&rankBy[order]=desc</pre>
        </li>
        <li>You need to ping Dex for the desired time. Use a cron job. ⏰</li>
        <li><span style="font-weight: bold; color: #ff5722;">NOTE:</span> This code is finetuned for Solana Tokens</li>
    </ol>

    <button id="addFilterButton" style="background-color: #1e88e5; color: white; padding: 10px 15px; border: none; border-radius: 5px; cursor: pointer; margin-top: 20px;">ADD FILTER</button>

    <!-- Modal overlay -->
    <div id="modalOverlay"></div>

    <div id="filterPopup">
        <h2>DEX FILTERS</h2>

        <div class="filter-group">
            <span class="filter-label">Chain:</span>
            <select id="chainSelect">
                <option value="">Select a chain</option>
                <option value="solana">Solana</option>
                <option value="base">Base</option>
                <option value="ethereum">Ethereum</option>
                <option value="bsc">BSC</option>
                <option value="avalanche">Avalanche</option>
                <option value="pulsechain">PulseChain</option>
                <option value="sonic">Sonic</option>
                <option value="ton">TON</option>
                <option value="custom">Custom Chain</option>
            </select>
        </div>

        <div class="filter-group" id="customChainGroup" style="display: none;">
            <span class="filter-label">Enter Your Desired Chain:</span>
            <input type="text" id="customChain" placeholder="Enter your desired chain">
        </div>

        <div class="filter-group">
            <span class="filter-label">Liquidity:</span>
            <div class="input-row">
                <div class="input-wrapper">
                    <span class="input-prefix">$</span>
                    <input type="text" placeholder="Min" inputmode="numeric" id="liquidityMin" oninput="formatNumber(this)">
                </div>
                <div class="input-wrapper">
                    <span class="input-prefix">$</span>
                    <input type="text" placeholder="Max" inputmode="numeric" id="liquidityMax" oninput="formatNumber(this)">
                </div>
            </div>
        </div>

        <div class="filter-group">
            <span class="filter-label">Market Cap:</span>
            <div class="input-row">
                <div class="input-wrapper">
                    <span class="input-prefix">$</span>
                    <input type="text" placeholder="Min" inputmode="numeric" id="marketCapMin" oninput="formatNumber(this)">
                </div>
                <div class="input-wrapper">
                    <span class="input-prefix">$</span>
                    <input type="text" placeholder="Max" inputmode="numeric" id="marketCapMax" oninput="formatNumber(this)">
                </div>
            </div>
        </div>

        <div class="filter-group">
            <span class="filter-label">FDV:</span>
            <div class="input-row">
                <div class="input-wrapper">
                    <span class="input-prefix">$</span>
                    <input type="text" placeholder="Min" inputmode="numeric" id="fdvMin" oninput="formatNumber(this)">
                </div>
                <div class="input-wrapper">
                    <span class="input-prefix">$</span>
                    <input type="text" placeholder="Max" inputmode="numeric" id="fdvMax" oninput="formatNumber(this)">
                </div>
            </div>
        </div>

        <div class="filter-group">
            <span class="filter-label">Pair Age (Hours):</span>
            <div class="input-row">
                <input type="text" placeholder="Min" inputmode="numeric" id="pairAgeMin" oninput="formatNumber(this)">
                <input type="text" placeholder="Max" inputmode="numeric" id="pairAgeMax" oninput="formatNumber(this)">
            </div>
        </div>

        <div class="filter-group">
            <span class="filter-label">24H Transactions:</span>
            <div class="input-row">
                <input type="text" placeholder="Min" inputmode="numeric" id="txns24Min" oninput="formatNumber(this)">
                <input type="text" placeholder="Max" inputmode="numeric" id="txns24Max" oninput="formatNumber(this)">
            </div>
        </div>

        <button id="submitFilters" style="background-color: #4caf50; color: white; padding: 10px 15px; border: none; border-radius: 5px; cursor: pointer; margin-top: 20px; width: 100%;">SUBMIT</button>
    </div>

    <div id="filterResult" style="margin-top: 20px;"></div>

    <script>
        function formatNumber(input) {
            // Remove non-numeric characters except for commas
            let value = input.value.replace(/[^0-9]/g, '');
            // Format the number with commas
            input.value = value.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }

        // Open popup when "ADD FILTER" button is clicked
        document.getElementById('addFilterButton').addEventListener('click', function() {
            document.getElementById('filterPopup').style.display = 'block';
            document.getElementById('modalOverlay').style.display = 'block';
        });

        // Show or hide the custom chain input based on selection
        document.getElementById('chainSelect').addEventListener('change', function() {
            const customChainGroup = document.getElementById('customChainGroup');
            customChainGroup.style.display = this.value === 'custom' ? 'block' : 'none';
        });

        // Close popup when clicking outside of it (on the modal overlay)
        document.getElementById('modalOverlay').addEventListener('click', function() {
            document.getElementById('filterPopup').style.display = 'none';
            document.getElementById('modalOverlay').style.display = 'none';
        });

        // Handle form submission and redirect to /dex with the filter string as a query parameter
        document.getElementById('submitFilters').addEventListener('click', function() {
            let chain = document.getElementById('chainSelect').value;
            if (chain === 'custom') {
                chain = document.getElementById('customChain').value;
            }

            let liquidityMin = document.getElementById('liquidityMin');
            let liquidityMax = document.getElementById('liquidityMax');
            let marketCapMin = document.getElementById('marketCapMin');
            let marketCapMax = document.getElementById('marketCapMax');
            let fdvMin = document.getElementById('fdvMin');
            let fdvMax = document.getElementById('fdvMax');
            let pairAgeMin = document.getElementById('pairAgeMin');
            let pairAgeMax = document.getElementById('pairAgeMax');
            let txns24Min = document.getElementById('txns24Min');
            let txns24Max = document.getElementById('txns24Max');

            let isValid = true;

            // Validate numeric inputs
            [liquidityMin, liquidityMax, marketCapMin, marketCapMax, fdvMin, fdvMax, pairAgeMin, pairAgeMax, txns24Min, txns24Max].forEach(input => {
                if (input.value && isNaN(input.value.replace(/,/g, ''))) {
                    input.classList.add('error');
                    isValid = false;
                } else {
                    input.classList.remove('error');
                }
            });

            if (!isValid) {
                return; // Don't proceed if invalid
            }

            let filterString = "wss://io.dexscreener.com/dex/screener/v5/pairs/h24/1?rankBy[key]=trendingScoreH6&rankBy[order]=desc";

            if (liquidityMin.value || liquidityMax.value) {
                filterString += `&filters[liquidity][min]=${liquidityMin.value.replace(/,/g, '') || ''}&filters[liquidity][max]=${liquidityMax.value.replace(/,/g, '') || ''}`;
            }
            if (marketCapMin.value || marketCapMax.value) {
                filterString += `&filters[marketCap][min]=${marketCapMin.value.replace(/,/g, '') || ''}&filters[marketCap][max]=${marketCapMax.value.replace(/,/g, '') || ''}`;
            }
            if (fdvMin.value || fdvMax.value) {
                filterString += `&filters[fdv][min]=${fdvMin.value.replace(/,/g, '') || ''}&filters[fdv][max]=${fdvMax.value.replace(/,/g, '') || ''}`;
            }
            if (pairAgeMin.value || pairAgeMax.value) {
                filterString += `&filters[pairAge][min]=${pairAgeMin.value.replace(/,/g, '') || ''}&filters[pairAge][max]=${pairAgeMax.value.replace(/,/g, '') || ''}`;
            }
            if (txns24Min.value || txns24Max.value) {
                filterString += `&filters[txns][h24][min]=${txns24Min.value.replace(/,/g, '') || ''}&filters[txns][h24][max]=${txns24Max.value.replace(/,/g, '') || ''}`;
            }
            if (chain) {
                filterString += `&filters[chainIds][0]=${chain}`;
            }

            // Redirect to /dex with the filter string as a query parameter
            window.location.href = "/dex?generated_text=" + encodeURIComponent(filterString);
        });
    </script>
</body>
</html>
