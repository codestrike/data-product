angular.module('a3app.controllers', [])
.controller('globalCtrl', function($rootScope, $http) {
  if(window.innerWidth < 768)
    $rootScope.isCollapsed = true;

  $rootScope.a3file = null; // data about uploaded file
})
.controller('signupCtrl', function($scope, $rootScope) {
  $rootScope.isSession = false;
  console.log('in signupCtrl now!');
})
.controller('plotCtrl', function($scope, $rootScope) {
  $rootScope.isSession = true;
  $scope.imageUrl = '';
  $scope.imageType = null;

  $scope.plotImage = function(imageType) {
    if($scope.imageType != imageType) {
      // $http.get() TODO
    }
  }
})
.controller('cleanupCtrl', function($scope, $rootScope, $http) {
  $rootScope.isSession = true;

  $scope.operations = [
  {'name':'misssing value', 'para':['cols','replace_by']},
  {'name':'replace value', 'para':['col', 'to_replace', 'replace_by']},
  {'name':'replace non number', 'para':['cols','replace_by','to_int']},
  {'name':'replace negative', 'para':['col','delete','replace_by']},
  {'name':'to upper', 'para':['col']},
  {'name':'to lower', 'para':['col']}
  ];

  $scope.selectedOperation = 0;
});