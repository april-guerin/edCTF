import Ember from 'ember';

export default Ember.Component.extend({
  challenge: {},
  modal: {},
  actions: {
    closeChallengeModal: function() {
      this.set('modal.isChallenge', false);
    },
  }
});