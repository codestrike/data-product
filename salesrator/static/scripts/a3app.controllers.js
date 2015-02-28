angular.module('a3app.controllers', [])
.controller('globalCtrl', function($rootScope, $http) {
  if(window.innerWidth < 768)
    $rootScope.isCollapsed = true;
  $rootScope.a3file = null; // data about uploaded file
  // console.log("We are in globalCtrl")

  // // $http.post('/api/cleanup',{hello:'world'}).success(function(r){
  //   $http.post('/api/cleanup', {msg:'hello word!'}).
  // success(function(data, status, headers, config) {
  //   // this callback will be called asynchronously
  //   console.log(data,"here is ");
  //   // when the response is available
  // });
  // });
})
.controller('plotCtrl', function($scope) {
  $scope.imageUrl = '';
  $scope.imageType = null;

  $scope.plotImage = function(imageType) {
    if($scope.imageType != imageType) {
      // $http.get() TODO
    }
  }
})
.controller('cleanupCtrl', function($scope, $http) {
  $scope.operations = [
  {'name':'misssing value', 'para':['cols','replace_by']},
  {'name':'replace value', 'para':['col', 'to_replace', 'replace_by']},
  {'name':'replace non number', 'para':['cols','replace_by','to_int']},
  {'name':'replace negative', 'para':['col','delete','replace_by']},
  {'name':'to upper', 'para':['col']},
  {'name':'to lower', 'para':['col']}
  ];

  $scope.selectedOperation = 0;
})