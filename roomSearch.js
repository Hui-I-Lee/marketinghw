let locationInput
let timeInputStart
let timeInputEnd

function searchRooms() {
    // 取得使用者輸入的地點和時間
    locationInput = document.getElementById("location").value;
    timeInputStart = document.getElementById("Starttime").value;
    timeInputEnd = document.getElementById("Endtime").value;

    // 在這裡根據地點和時間執行查詢，並顯示結果
    // 這裡只是一個簡單的範例，使用模擬數據
    const mockData = [
        { location: 'Berlin', type: 'single room', price: 400 },
        { location: 'Berlin', type: 'double room', price: 450 },
        { location: 'Berlin', type: 'apartment', price: 600 },
        { location: 'Karlsruhe', type: 'single room', price: 100 },
        { location: 'Karlsruhe', type: 'double room', price: 150 },
        { location: 'Karlsruhe', type: 'apartment', price: 200 },
        { location: 'Munich', type: 'single room', price: 300 },
        { location: 'Munich', type: 'double room', price: 350 },
        { location: 'Munich', type: 'apartment', price: 500 }
    ];
    //const inputData = 'Berlin'; // Replace 'Berlin' with the actual input from the user
    let filteredData;

    if (locationInput === 'Berlin') {
        filteredData = mockData.filter(item => item.location === 'Berlin');
    } else if (locationInput === 'Munich') {
        filteredData = mockData.filter(item => item.location === 'Munich');
    } else {
        filteredData = mockData.filter(item => item.location === 'Karlsruhe');
    }

    //console.log(filteredData);


    displayResults(filteredData);

    // 將請求發送到後端
    /*
    fetch(`/api/rooms?location=${locationInput}&time=${timeInput}`)
        .then(response => response.json())
        .then(data => displayResults(data))
        .catch(error => console.error('Error:', error));*/
}

function displayResults(data) {
    var resultDiv = document.getElementById("result");

    /*resultDiv.innerHTML = `<p>From ${timeInputStart} to ${timeInputEnd} , room for ${locationInput} include</p>
                            ${data.map(room => `<button onclick="selectRoom('${room.type}', ${room.price})">${room.type} - $${room.price}</button><br>`).join('')}`;
*/
    resultDiv.innerHTML = `<p>From ${timeInputStart} to ${timeInputEnd} , room for ${locationInput} include</p>
                            ${data.map(room => `<button onclick="selectRoom('${room.type}', ${room.price})">${room.type} - $${room.price}</button><br>`).join('')}`;

}
function selectRoom(type, price) {
    // Add your logic for handling the selected room
    console.log(`Selected room: ${type} - $${price}`);

    // For demonstration purposes, let's assume you want to redirect to a payment page
    redirectToPayment(type, price);
}

function createPaymentButton(type, price) {
    var resultDiv = document.getElementById("result");

    // Create a button element
    var paymentButton = document.createElement('button');
    paymentButton.textContent = 'Proceed to Payment';

    // Attach a click event listener to the button
    paymentButton.addEventListener('click', function () {
        // Redirect to the payment page or perform other actions
        redirectToPayment(type, price);
    });

    // Append the button to the resultDiv
    resultDiv.appendChild(paymentButton);
}

function redirectToPayment(type, price) {
    // You can customize this function based on your payment handling logic
    // For now, let's simulate a redirect to a payment page
    if (type === 'single room') {
        window.location.href = 'single.html'
        //window.location.href = 'payment.html'
    } else if (type === 'double room') {
        window.location.href = 'double.html'
    } else {
        window.location.href = 'apartment.html'
    }
    //alert(`Redirecting to payment for ${type} - $${price}`);
    // You can replace the alert with actual redirection logic
}

/*
function processPayment() {
    // Add your logic for processing the payment
    var cardNumber = document.getElementById("cardNumber").value;
    var expirationDate = document.getElementById("expirationDate").value;

    if (validatePaymentInput(cardNumber, expirationDate)) {
        alert('Payment processed successfully!');
        // You can replace the alert with actual payment processing logic
    } else {
        alert('Invalid payment details. Please check your input.');
    }
}

function validatePaymentInput(cardNumber, expirationDate) {
    // Add your validation logic here (e.g., check if the card number and date are valid)
    // For simplicity, this example only checks if the fields are non-empty
    return cardNumber.trim() !== '' && expirationDate.trim() !== '';
}*/