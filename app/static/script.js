 // Fetch all expenses from backend and display
        async function fetchExpenses() {
            try {
                const response = await fetch('/expenses');
                const data = await response.json();
                displayExpenses(data);
            } catch (error) {
                console.error('Error fetching expenses:', error);
            }
        }

        // Handle adding a new expense
        document.getElementById('expense-form').addEventListener('submit', async function(event) {
            event.preventDefault();

            const id = parseInt(document.getElementById('id').value);
            const desc = document.getElementById('desc').value;
            const amount = parseFloat(document.getElementById('amount').value);
            const dateValue = document.getElementById('date').value;

            // Convert month input to full date (first day of month)
            const date = new Date(dateValue + '-01');

            const expense = { id: id, title: desc, amount: amount, date: date };

            try {
                const response = await fetch('/expenses', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(expense)
                });
                await response.json();
                fetchExpenses();  // Refresh list
                document.getElementById('expense-form').reset();
            } catch (error) {
                console.error('Error adding expense:', error);
            }
        });

        // Display expenses in the browser
        function displayExpenses(expenses) {
            const list = document.getElementById('expense-list');
            list.innerHTML = '';
            expenses.forEach(exp => {
                const item = document.createElement('li');
                const expDate = new Date(exp.date);
                item.textContent = `ID: ${exp.id}, Description: ${exp.title}, Amount: ₹${exp.amount}, Date: ${expDate.getMonth()+1}/${expDate.getFullYear()}`;
                list.appendChild(item);
            });
        }

        // Get monthly total from backend
        async function getMonthlyTotal() {
            const searchId = parseInt(document.getElementById('search-id').value);
            const monthInput = document.getElementById('search-month').value;

            let month, year;
            if (monthInput) {
                const parts = monthInput.split('-');
                year = parseInt(parts[0]);
                month = parseInt(parts[1]);
            }

            try {
                const url = `/expenses/summary/${searchId}` + 
                            (month ? `?month=${month}&year=${year}` : '');
                const response = await fetch(url);
                const data = await response.json();
                document.getElementById('total-output').textContent =
                    `Total expense for ID ${data.user_id} in ${data.month}/${data.year}: ₹${data.total}`;
            } catch (error) {
                console.error('Error fetching monthly total:', error);
            }
        }

        // Initial load
        fetchExpenses();
