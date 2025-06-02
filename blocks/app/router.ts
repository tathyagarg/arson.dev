import EmberRouter from '@ember/routing/router';
import config from 'blocks/config/environment';

export default class Router extends EmberRouter {
  location = config.locationType;
  rootURL = config.rootURL;
}

Router.map(function () {
  this.route('project', function() {
    this.route('index', { path: '/' });
  });
});
