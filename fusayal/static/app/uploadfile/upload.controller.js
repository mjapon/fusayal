(function () {
    'use strict';
    angular.module("isyplus")

        .controller("UploadCntrl", UploadCntrl);

    function UploadCntrl($scope, NotifServ, $state) {

        var vm = $scope;
        vm.form = {nombreArchivo: ''};

        init();

        function init() {
            console.log("upload controller init-->");
        }


    }

})();