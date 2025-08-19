let editingId = null;

// Fetch all expenses and display
async function fetchExpenses() {
    try {
        const response = await fetch('/expenses');
        const data = await response.json();
        displayExpenses(data);
    } catch (error) {
        console.error('Error fetching expenses:', error);
    }
}

// Handle adding or editing an expense
document.getElementById('expense-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const user_id = parseInt(document.getElementById('user_id').value);
    const title = document.getElementById('desc').value;
    const amount = parseFloat(document.getElementById('amount').value);
    const dateValue = document.getElementById('date').value;
    const date = dateValue ? new Date(dateValue) : null;
    const expense = { user_id, title, amount, date };

    try {
        if (editingId) {
            // Update expense
            await fetch(`/expenses/${editingId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(expense)
            });
            editingId = null;
        } else {
            // Add new expense
            await fetch('/expenses', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(expense)
            });
        }
        fetchExpenses();
        document.getElementById('expense-form').reset();
    } catch (error) {
        console.error('Error adding/updating expense:', error);
    }
});

// Display expenses
function displayExpenses(expenses) {
    const list = document.getElementById('expense-list');
    list.innerHTML = '';

    expenses.forEach(exp => {
        const item = document.createElement('li');
        const expDate = new Date(exp.date);
        item.innerHTML = `
            User ID: ${exp.user_id}, Description: ${exp.title}, Amount: ₹${exp.amount}, Date: ${expDate.getMonth()+1}/${expDate.getFullYear()}
            <button onclick="editExpense(${exp.id}, ${exp.user_id}, '${exp.title}', ${exp.amount}, '${expDate.toISOString().split('T')[0]}')">Edit</button>
            <button onclick="deleteExpense(${exp.id})">Delete</button>
        `;
        list.appendChild(item);
    });
}

// Delete expense
async function deleteExpense(id) {
    try {
        await fetch(`/expenses/${id}`, { method: 'DELETE' });
        fetchExpenses();
    } catch (error) {
        console.error('Error deleting expense:', error);
    }
}

// Edit expense
function editExpense(id, user_id, title, amount, dateValue) {
    editingId = id;
    document.getElementById('user_id').value = user_id;
    document.getElementById('desc').value = title;
    document.getElementById('amount').value = amount;
    document.getElementById('date').value = dateValue;
}

// Get monthly total
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
            `Total expense for User ID ${data.user_id} in ${data.month}/${data.year}: ₹${data.total}`;
    } catch (error) {
        console.error('Error fetching monthly total:', error);
    }
}

// Initial load
fetchExpenses();
