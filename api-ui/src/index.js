import {hello} from "./greet";

const register = (registerRequest) => {
    console.log(registerRequest)
}

const registerBtn = document.querySelector('button.register');

registerBtn.addEventListener('click', () => {
    register({"name": "Tomek", "xyz": 'foo'});
});

(() => {
    hello("Tomek :)");
})();