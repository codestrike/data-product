/* global angular */

angular.module('a3app.controllers', ['ngCookies'])
.controller('globalCtrl', function($cookies, $http, $rootScope, $scope, $state) {
  $scope.inSession = false;
  $rootScope.inSession = $scope.inSession;
  $scope.a3files = null; // data about uploaded file
  $scope.selectedStamp = null;
  $scope.allColumns = [];

  if(window.innerWidth < 768)
    $scope.isCollapsed = true;
  else
    $scope.isCollapsed = false;

  $scope.setA3files = function(filesList) {
    $scope.a3files = filesList;
  };

  $scope.setStamp = function(stamp) {
    $scope.selectedStamp = stamp;
    $scope.$broadcast('a3optionsAvailabel');
  };

  $scope.fetchData= function(dataToFetch, callback) {
    $http.post('/api/userdata', {
      info: dataToFetch
    }).success(function(res) {
      if (angular.isFunction(callback)) {
        callback(res);
      }
    }).error(function(res, sta) {
      console.error(sta, res);
    });
  };

  $scope.getOperations = function(callback) {
    $http.get('/api/operations').success(function(res) {
      for (var i = res.length - 1; i >= 0; i--) {
        res[i].name = res[i].operation.replace(/_/g, ' ');
      }
      $scope.operations = res;
      if (angular.isFunction(callback))
        callback();
      $scope.$broadcast('a3optionsAvailabel');
    });
  };

  $scope.showSidebar = function(yes) {
    $scope.inSession = yes;
  };

  $scope.getCurrrentStatus = function() {
    if (!$scope.operations) return;
    if ($scope.allColumns === 'working') return;
    $scope.allColumns = 'working';

    var toSend = {};
    for (var i = $scope.operations.length - 1; i>=0; i--) {
      var o = $scope.operations[i];
      if (o.operation === 'describe_all') {
        toSend = o;
        break;
      }
    }

    // if (toSend === {}) return;

    toSend.para = {};
    $http.post('/api/cleanup', toSend)
    .success(function(res) {
      $scope.allColumns = [];
      angular.forEach(res, function(value, key) {
        this.push({
          name: key,
          attrs: value
        });
      }, $scope.allColumns);
    });

  };

  // $scope.getCurrrentStatus();
  $scope.$on('a3optionsAvailabel', $scope.getCurrrentStatus);

  // call initialization functions
  if($cookies.auth_tkt) {
    $scope.getOperations();

    $scope.fetchData('user', function(res) {
      $scope.setStamp(res.stamp);
    });
  }

  // event listeners
  $rootScope.$on('$stateChangeStart', function(ev, toState, toPara) {
    if(!$cookies.auth_tkt && toState.name != 'app.login' && toState.name != 'app.signup') {
      if (toPara.fromLogin != 'yes') {
        console.log('Permission Denied 403');
        ev.preventDefault();
        $state.go('app.login');
      } else {
        console.log('First Login Allow');
      }
    } else if(!!$cookies.auth_tkt && (toState.name == 'app.login' || toState.name == 'app.signup') ) {
      ev.preventDefault();
      $state.go('app.dash');
    }
  });
})
.controller('loginCtrl', function($cookies, $http, $scope, $state, $templateCache, $timeout) {
  $templateCache.removeAll();
  $scope.showSidebar(false);

  if($cookies.auth_tkt && $cookies.auth_tkt.length > 0)
    $state.go('app.dash', {fromLogin:'yes'});

  $scope.tryLogin = function() {
    if($scope.loginform.$valid) {
      $http.post('/api/login', {
        email: $scope.email,
        passwd: $scope.passwd
      }).success(function(res) {
        console.log('LOGIN SUCCESS', res);
        if(res.status == 'success') {
          $scope.getOperations(function() {
            console.log('Login SUCCESS; Redirecting to dash');
            $state.go('app.dash', {fromLogin:'yes'});
          });
        } else {
          // Show Error Message
          $scope.errorMessage = 'Wrong Credentials';
          $timeout(function() {
            $scope.errorMessage = '';
          }, 5000);
          $scope.passwd = '';
        }
      });
    }
  };
})
.controller('signupCtrl', function($http, $scope, $state, $timeout) {
  $scope.showSidebar(false);
  $scope.doSignup = function() {
    if($scope.signupform.$valid) {
      $http.post('/api/signup', {
        name: $scope.name,
        email: $scope.email,
        passwd: $scope.passwd
      }).success(function(res) {
        if(res.status == 'success') {
          if(res.u3id != null) {
            // ACCOUNT CREATED SUCCESSFULLY
            $scope.displayMessage = 'Account Created.';
            $timeout(function() {
              $state.go('app.login');
            }, 5000);
          } else {
            $scope.displayMessage = 'This Email ID Is Already Used.';
          }
        } else {
          $scope.displayMessage = 'Unable To Create New Account.';
        }

        $timeout(function() {
          $scope.displayMessage = '';
        }, 10000);
      }).error(function(res, status) {
        console.log('SIGNUP FAIL', status, res);
      });
    }
  };
})
.controller('dashCtrl', function($http, $scope){
  $scope.showSidebar(true);

  $scope.fetchFilesData = function(callback) {
    $scope.fetchData('files', function(res) {
      $scope.setA3files(res);
      if (angular.isFunction(callback)) 
        callback(res);
    });
  };

  $scope.fetchUserData = function() {
    $scope.fetchData('user', function(res) {
      console.log('USER DATA FETCHED', res);
      $scope.setStamp(res.stamp);
    });
  };
  
  $scope.updateFile = function(operation, stamp) {
    $http.post('/api/fileupdate', {
      'operation': operation,
      'stamp': stamp
    }).success(function() {
      $scope.fetchFilesData();

      if (operation === 'set') {
        $scope.setStamp(stamp);
      } else if (operation === 'remove') {
        $scope.fetchUserData();
      }
    }).error(function(res, sta) {
      console.error(sta, res);
    });
  };

  // call initialization functions
  $scope.fetchFilesData($scope.fetchUserData);
})
.controller('plotCtrl', function($http,$scope) {
  $scope.showSidebar(true);
  $scope.imageUrl = '';
  $scope.imageType = null;
  $scope.onX = 0;
  $scope.onY = 0;
  $scope.ylim = 1000;
  $scope.getCurrrentStatus();

  $scope.doPlot = function(imageType) {
    var toSend = {
      onx: $scope.onX,
      ony: $scope.onY,
      ylim: $scope.ylim
    };

    console.log("toSendAPI",toSend);
    $http.post('/api/plot',toSend)
    .success(function(res){
      $scope.imageBase64 = res.base64;
      console.log($scope.imageBase64);
    });
  };
})
.controller('cleanupCtrl', function($http, $scope) {
  $scope.showSidebar(true);
  $scope.selectedOperation = 0;
  $scope.params = {};

  $scope.resetParams = function() {
    $scope.params = {};
  };

  $scope.performOperation = function() {
    console.log($scope.cleanupform.$valid);
    console.log($scope.selectedOperation, $scope.operations[$scope.selectedOperation]);
    console.log($scope.params);
    var toSend = $scope.operations[$scope.selectedOperation] ;
    toSend.para = $scope.params;

    $http.post('/api/cleanup',toSend )
    .success(function(res){
    	console.log(res);
    });
  };

  
  // call initialization functions
  $scope.getCurrrentStatus();

  
});
