import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('scoreboard');
  this.route('about');
  this.route('challenges');
  this.route('challenges', function() {});
  this.route('modal');
});

export default Router;
