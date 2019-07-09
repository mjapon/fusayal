(function () {
    'use strict';
    angular.module("isyplus")
        .controller("AutorizacionFormCntrl", AutorizacionFormCntrl);

    function AutorizacionFormCntrl($scope, $state, AutorizacionServ, NotifServ, focusService) {

        var vm = $scope;

        vm.form = {};
        vm.contribsel = {};
        vm.listas ={contributentes:[], tiposdoc:[]};

        vm.guardar = guardar;
        vm.cancelar = cancelar;
        vm.onContribSel = onContribSel;

        init();
        
        function init() {
            var res = AutorizacionServ.get({aut_id:0}, function(){
                if (res.estado == 200){
                    vm.form = res.form;
                    vm.listas.contributentes = res.contribs;
                    vm.listas.tiposdoc = res.tiposdoc;
                }
            });

            focusService.setFocus("contrib",1000);
        }

        function guardar() {
            var res = AutorizacionServ.save(vm.form, function(){
                if (res.estado === 200){
                    NotifServ.success(res.msg);
                    $state.go("auts_list");
                }
            });
        }

        function onContribSel(contribsel){
            if (contribsel){
                vm.form.cnt_id = contribsel.cnt_id;
                focusService.setFocus("aut_estab", 100);
            }
        }

        function cancelar() {
            $state.go("auts_list");
        }
    }
})();