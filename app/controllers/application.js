import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  authController: undefined,
  actions: {
    login: function(authenticationData) {
      this.get('authController').login(authenticationData);
      this.set('modal.isLogin', false);
    },
    logout: function(authenticationData) {
      this.get('authController').logout();
    },
    openLoginModal: function() {
      this.set('modal.isLogin', true);
    },
    openRegisterModal: function() {
      this.set('modal.isRegister', true);
    },
  }
});