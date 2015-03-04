angular.module('a3app.controllers', ['ngCookies'])
.controller('globalCtrl', function($cookies, $http, $rootScope, $scope, $state) {
  $scope.inSession = false;
  $rootScope.inSession = $scope.inSession;
  $scope.a3file = null; // data about uploaded file

  if(window.innerWidth < 768)
    $scope.isCollapsed = true;
  else
    $scope.isCollapsed = false;

  if(!angular.isDefined($scope.operations)) {
    $http.get('/api/operations').success(function(res) {
      for (var i = res.length - 1; i >= 0; i--) {
        res[i].name = res[i].operation.replace(/_/g, ' ');
      };
      $scope.operations = res;
    });
  }

  $scope.showSidebar = function(yes) {
    $scope.inSession = yes;
  };

  $rootScope.$on('$stateChangeStart', function(ev, toState, toPara, fromState) {
    if(!$cookies.auth_tkt && toState.name != 'app.login' && toState.name != 'app.signup') {
      console.log('Permission Denied 403');
      ev.preventDefault();
      $state.go('app.login');
    }
  });
})
.controller('loginCtrl', function($http, $scope, $state, $templateCache, $timeout) {
  $templateCache.removeAll();
  $scope.showSidebar(false);

  $scope.try_login = function() {
    if($scope.loginform.$valid) {
      $http.post('/api/login', {
        email: $scope.email,
        passwd: $scope.passwd
      }).success(function(res) {
        console.log('LOGIN SUCCESS', res);
        if(res.status == 'success') {
          $state.go('app.cleanup');
        } else {
          // Show Error Message
          $scope.errorMessage = 'Wrong Credentials';
          $timeout(function() {
            $scope.errorMessage = '';
          }, 5000);
          $scope.passwd = ''
        }
      });
    }
  };
})
.controller('signupCtrl', function($http, $scope) {
  $scope.showSidebar(false);
  $scope.doSignup = function() {
    if($scope.signupform.$valid) {
      $http.post('/api/signup', {
        name: $scope.name,
        email: $scope.email,
        passwd: $scope.passwd
      }).success(function(res) {
        console.log("SIGNUP SUCCESS", res);
      }).error(function(res, status) {
        console.log("SIGNUP FAIL", status, res);
      })
    }
  }
})
.controller('plotCtrl', function($scope) {
  $scope.showSidebar(true);
  $scope.imageUrl = '';
  $scope.imageType = null;

  $scope.plotImage = function(imageType) {
    if($scope.imageType != imageType) {
      // $http.get() TODO
    }
  }
})
.controller('cleanupCtrl', function($http, $scope) {
  $scope.showSidebar(true);
  $scope.selectedOperation = 0;
  $scope.params = {};
  $scope.allColumns = [
    {'name':'q1', 'attrone':'something', 'attrtwo':'value of it'},
    {'name':'q2', 'attrone':'something', 'attrtwo':'value of it'},
    {'name':'q3', 'attrone':'something', 'attrtwo':'value of it'},
    {'name':'q4', 'attrone':'something', 'attrtwo':'value of it'},
    {'name':'q5', 'attrone':'something', 'attrtwo':'value of it'},
    {'name':'q6', 'attrone':'something', 'attrtwo':'value of it'},
    {'name':'q7', 'attrone':'something', 'attrtwo':'value of it'},
    {'name':'q8', 'attrone':'something', 'attrtwo':'value of it'}
    ];

  $scope.resetParams = function() {
    $scope.params = {};
  }

  $scope.performOperation = function() {
    console.log($scope.cleanupform.$valid);
    console.log($scope.selectedOperation, $scope.operations[$scope.selectedOperation]);
    console.log($scope.params);
  }

});
