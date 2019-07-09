(function () {
    'use strict';
    angular.module("isyplus")
        .controller("ReportesCntrl", ReportesCntrl);

    function ReportesCntrl($scope) {

        var vm = $scope;

        init();

        function init() {
            console.log("Reportes Cntrl Init executed-->");
        }
    }

})();