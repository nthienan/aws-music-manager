/**
 * @author nthienan
 */
// song controller
mainApp.controller('songCtrl', function ($rootScope, $scope, $http, $location, $filter, ngProgress, $translate, langService, globalConfig) {
        $scope.selectedId = [];
        $http.defaults.headers.post['Content-Type'] = 'application/json';

        // sort
        var orderBy = $filter('orderBy');
        $scope.order = function (predicate, reverse) {
            $rootScope.songResponse.content = orderBy($rootScope.songResponse.content, predicate, reverse);
            switch (predicate) {
                case 'id':
                    $scope.id = reverse ? 'glyphicon-sort-by-attributes-alt' : 'glyphicon-sort-by-attributes';
                    $scope.name = '';
                    $scope.gener = '';
                    break;
                case 'name':
                    $scope.name = reverse ? 'glyphicon-sort-by-attributes-alt' : 'glyphicon-sort-by-attributes';
                    $scope.id = '';
                    $scope.gener = '';
                    break;
                case 'gener':
                    $scope.gener = reverse ? 'glyphicon-sort-by-attributes-alt' : 'glyphicon-sort-by-attributes';
                    $scope.name = '';
                    $scope.id = '';
                    break;
            }
        };

        // load list
        $scope.load = function () {
            ngProgress.start();
            $http.get(globalConfig.baseURL + '/' + $rootScope.user.email + '/song' + '?page=' + ($rootScope.pageNumber - 1) + '&size=' + $rootScope.pageSize)
                .success(function (data) {
                    $rootScope.songResponse = data;
                    ngProgress.complete();
                })
                .error(function (data, status) {
                    console.log(status + data);
                    ngProgress.complete();
                });
        };

        $scope.create = function () {
            ngProgress.start();
            if ($scope.shared == undefined)
                $scope.shared = false;
            reader = new FileReader();
            reader.onload = function () {
                var f = new Uint8Array(reader.result);
                $http({
                    method: 'POST',
                    url: globalConfig.baseURL + '/song/upload',
                    headers: {'Content-Type': "application/octet-stream"},
                    data: f,
                    transformRequest: []
                }).success(function (data) {
                    $http({
                        method: 'POST',
                        url: globalConfig.baseURL + '/song',
                        headers: {'Content-Type': "application/json"},
                        data: JSON.stringify({
                            name: $scope.name,
                            genre: $scope.genre,
                            file: data.path,
                            shared: $scope.shared,
                            owner: $rootScope.user.email
                        })
                    }).success(function (data) {
                        ngProgress.complete();
                        $location.path("/");
                    }).error(function (data, status) {
                        ngProgress.complete();
                    })
                }).error(function (data, status) {
                    ngProgress.complete();
                });
            };
            reader.readAsArrayBuffer(document.forms['formUpload'].file.files[0]);
        };

        // delete
        $scope.deleteMulti = function () {
            ngProgress.start();
            var values = JSON.stringify($scope.selectedId);
            jQuery.ajax({
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                'type': 'DELETE',
                'url': '/api/song/' + $rootScope.user.username,
                'data': values,
                'dataType': 'json'
            })
                .success(function (data) {
                    ngProgress.complete();
                    $scope.load();
                })
                .error(function (data, status) {
                    ngProgress.complete();
                });
        };

        // play
        $scope.playSong = function (id) {
            ngProgress.start();
            $http.put('/api/song/' + id + '/view')
                .success(function (data) {
                    ngProgress.complete();
                    $location.path('/play-song/' + id);
                })
                .error(function (data, status) {
                    ngProgress.complete();
                });
        };

        // push or splice selected id
        $scope.select = function (id) {
            var idx = $scope.selectedId.indexOf(id);
            if (idx > -1)
                $scope.selectedId.splice(idx, 1);
            else
                $scope.selectedId.push(id);
        };

        // redirect to edit view
        $scope.editSong = function (id) {
            $location.path('/edit-song/' + id);
        };

        $scope.back = function () {
            $location.path('/');
        };

        $scope.$on('langBroadcast', function () {
            $translate.use(langService.key);
        });

        $scope.load();
    }
);