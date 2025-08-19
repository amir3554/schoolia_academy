function switchPaymentMethod(type, content) {
    const stripeCard = document.getElementById('stripe-card');
    const stripePaymentElement = document.getElementById('payment-element');

    if (type === 'stripe') {
    stripeCard.style.display = 'block'
    
    } else {
    stripeCard.style.display = 'none'
    stripePaymentElement.innerHTML = ''
    
    }
}

