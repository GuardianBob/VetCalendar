/*
Author: Jesse with inputs from Joey
Some of these will allow for an input to remain blank and still be valid
In order for an input to be required, make sure to add the "required" rule.

In order to add these, import ValidateService to your page.
create a function to set the rules by adding this under "methods":
    getValidators() {
        this.rules = (ValidateService.validators)
    }

Call the getValidators() function by adding it to "created()":
    this.getValidators();

*/
class ValidateService {  
  constructor() {
    this.validators = {
      // Ensures field is set as required
      required: value => !!value || 'Required.',
      
      // max of 50 characters allowed
      max50: value => value.length <= 50 || 'Max 50 characters',
      
      // max of 255 characters allowed
      max255: value => value.length <= 255 || 'Max 255 characters',
      
      // Email validator
      // Allows for field to remain blank if not using required rule as well
      email: value => {
        // const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        // if (!value) {
        // return true
        // } else {
        // return pattern.test(value) || 'Invalid e-mail.'
        // }
        // ABOVE WORKS, BELOW IS SIMPLIFIED VERSION
        const pattern = /^\S+@\S+\.\S+$/;
        return !value || pattern.test(value) || 'Invalid e-mail.';
      },
      
      // Phone validator
      // Works with international numbers as well
      // Allows for field to remain blank if not using required rule as well
      phone: value => {
        const pattern = /^[+]?[0-9]{0,3}?[-\s.(]?[0-9]{3}?[)-\s.]?[\s]?[0-9]{3}[-\s.]?[0-9]{4,6}$/im
        if (!value) {
        return true
        } else {
        return pattern.test(value) || 'Invalid phone number.'
        }
      },

      color: value => {
        const hex3Pattern = /^#([A-Fa-f0-9]{3})$/i;
        const hex6Pattern = /^#([A-Fa-f0-9]{6})$/i;
        const rgbPattern = /^rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)$/i;
        return !value || hex3Pattern.test(value) || hex6Pattern.test(value) || rgbPattern.test(value) || 'Invalid color option.';
      },

      // Password Validators
      // Multiple options depending on what is required by client.
      // Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character:
      pass_all: value => {
        const pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
        if (!value) {
          return true
        } else {
          return pattern.test(value) || 'Password must contain a minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character.'
        }
      },

      // Minimum eight characters, at least one letter and one number:
      pass_a_1: value => {
        const pattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/
        if (!value) {
          return true
        } else {
          return pattern.test(value) || 'Password must contain a minimum eight characters, at least one letter and one number'
        }
      },

      // Minimum eight characters, at least one letter, one number and one special character
      pass_a_1_sp: value => {
        const pattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/
        if (!value) {
          return true
        } else {
          return pattern.test(value) || 'Password must contain a minimum eight characters, at least one letter, one number and one special character'
        }
      },

      //Minimum eight characters, at least one uppercase letter, one lowercase letter and one number:
      pass_a_1_up: value => {
        const pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/
        if (!value) {
          return true
        } else {
          return pattern.test(value) || 'Password must contain a minimum eight characters, at least one uppercase letter, one lowercase letter and one number'
        }
      },
      
      // Zip code validator
      // works with additional "-####" that postal service uses
      zip: value => {
        const pattern = /^\d{5}$|^\d{5}-\d{4}$/
        return pattern.test(value) || 'Invalid zip code.'
      },
      
      // name validator that allows dashes
      name: value => {
          const pattern = /^[-\w]+$/
          return pattern.test(value) || 'Invalid input'
      },
      
      // alpha validator that allows: - , . and spaces
      alpha_char: value => {
        const pattern = /^[-,.\w\s]+$/
        if (!value) {
          return true
        } else {
          return pattern.test(value) || 'Invalid input'
        }
      },
      
      // alpha validator that allows only alpha
      alpha: value => {
        const pattern = /^[\w]+$/
        if (!value) {
        return true
        } else {
        return pattern.test(value) || 'Invalid input.'
        }
      },

      numeric: value => {
        const pattern = /^\d+$/
        if (!value) {
        return true
        } else {
        return pattern.test(value) || 'Invalid input.'
        }
      },
      
      // alphanumeric validator
      alphanumeric: value => {
        const pattern = /^[\w\d]+$/
        if (!value) {
        return true
        } else {
        return pattern.test(value) || 'Invalid input.'
        }
      }
    }
  }
}
export default new ValidateService();