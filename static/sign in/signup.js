
/// error messages
  const form = document.getElementById('form')
  const firstname_input = document.getElementById('firstname-input')
  const email_input = document.getElementById('email-input')
  const password_input = document.getElementById('password-input')
  const repeat_password_input = document.getElementById('repeat-password-input')
  const username_input = document.getElementById('username-input')

  form.addEventListener('submit', (e) => {

    let errors = []
    if(firstname_input){
        //firstname input -> signup
        errors = getSignedupFormErrors(firstname_input.value, email_input.value, password_input.value, repeat_password_input.value)
    }
    else {
        //no firstname -> login
        errors = getLoginFormErrors(username_input.value, password_input.value)
    }

    if(errors.length > 0){
        //if there are any errors -> don't submit
        e.preventDefault()
    }
  })

  function getSignedupFormErrors(firstname, email, password, repeatPassword){
    let errors = []

    if(firstname === '' || firstname == null){
        errors.push('First Name is required')
        firstname_input.parentElement.classList.add('incorrect')
    }
    if(email === '' || email == null){
        errors.push('Email is required')
        email_input.parentElement.classList.add('incorrect')
    }
    if(password === '' || password == null){
        errors.push('Password is required')
        password_input.parentElement.classList.add('incorrect')
    }

    return errors;
  }