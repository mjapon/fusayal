# coding: utf-8
"""
Fecha de creacion 3/16/19
@autor: mjapon
"""
import logging
from datetime import datetime

from fusayal.logica.dao.base import BaseDao
from fusayal.logica.excepciones.validacion import ErrorValidacionExc
from fusayal.logica.roles.tuserrol_dao import TUserRolDao
from fusayal.logica.users.users_model import TUser
from fusayal.utils import cadenas

log = logging.getLogger(__name__)


class TUsersDao(BaseDao):

    def autenticar(self, username, password):
        """
        Autentica un usuario en el sistema
        :param username:
        :param password:
        :return:
        """

        """
        'idUser': 0,
                'nomApel': '',
                'nombrecuenta': '',
                'claveTemp': '',
                'confClaveTemp': ''
        """

        sql = "select count(*) as cuenta from tuser where us_name = '{0}' and us_pass = '{1}' and us_status = 0".format(username,
                                                                                                                   password)
        log.info("sql que se ejecuta es:")
        log.info(sql)

        cuenta = self.first_col(sql=sql, col="cuenta")
        return cuenta > 0

    def get_user(self, username):
        return self.dbsession.query(TUser).filter(TUser.us_name==username).first()


    def existe(self, username):
        """
        Verifica si un nombre de usuario ya esta registrado en el sistema
        :param username:
        :return:
        """
        sql = "select count(*) as cuenta from tuser where us_name = '{0}'".format(username)
        cuenta = self.first_col(sql=sql, col="cuenta")
        return cuenta > 0

    def cambiar_clave(self, user_name, password, rpassword):
        """
        Actualiza  la clave de un usuario en el sistema
        :param user_name:
        :param password:
        :param rpassword:
        :return:
        """
        tuser = self.find_by_username(username=user_name.strip())
        if tuser is not None:
            #Verificar que las claves ingresadas coincida
            if password != rpassword:
                raise ErrorValidacionExc("Las claves ingresadas no coinciden")

            if password is None or len(password.strip()) < 4:
                raise ErrorValidacionExc("Por favor ingrese la clave, debe ser mínimo de 4 caracteres")

            if password == tuser.us_pass:
                raise ErrorValidacionExc("La clave ingresada no puede ser la misma que se le asignó")

            tuser.us_pass = password
            tuser.us_statusclave = 1

    def crear_usuario(self, user_name, nomapel, password, rpassword, roles=None):
        """
        Registra un nuevo usuario en el sistema
        :param user_name:
        :param password:
        :param rpassword:
        :param roles:
        :return:
        """

        if not cadenas.es_nonulo_novacio(user_name):
            raise ErrorValidacionExc("Debe ingresar el nombre de usuario")
        if not cadenas.es_nonulo_novacio(nomapel):
            raise ErrorValidacionExc("Debe ingresar los apellidos y nombres del usuario")
        if not cadenas.es_nonulo_novacio(password):
            raise ErrorValidacionExc("Debe ingresar la clave inicial")
        if not cadenas.es_nonulo_novacio(rpassword):
            raise ErrorValidacionExc("Ingrese la confirmación del clave")


        if self.existe(user_name):
            raise ErrorValidacionExc("Ya existe una cuenta de usuario con el nombre:{0}, elija otro".format(user_name))

        if password is None or len(password.strip())<4:
            raise ErrorValidacionExc("Por favor ingrese la clave, debe ser mínimo de 4 caracteres")

        if (password != rpassword):
            raise ErrorValidacionExc("Las claves ingresadas no coinciden, favor verificar")

        tuser = TUser()
        tuser.us_name = user_name
        tuser.us_pass = password
        tuser.us_datecreated = datetime.now()
        tuser.us_status = 0 #
        tuser.us_statusclave = 0
        tuser.us_nomapel = nomapel.upper()

        self.dbsession.add(tuser)
        self.dbsession.flush()

        #Registro de la matriz de roles
        tuserroldao = TUserRolDao(self.dbsession)
        tuserroldao.asociar(us_id=tuser.us_id, roles_list=roles)


    def find_by_username(self, username):
        """
        Busca un usuario por su nombe de cuenta
        :param username:
        :return:
        """
        tuser = self.dbsession.query(TUser).filter(TUser.us_name == username)
        return tuser

    def listar(self):
        """
        Retorna todos los usuarios registrados en el sistema
        :return:
        """

        sql = """
        select us_id, us_name, us_nomapel, us_datecreated, us_status,
        case when us_status = 0 then 'ACTIVO' when us_status = 1 then 'INACTIVO' else 'ND' end as estado 
        from tuser ORDER BY us_nomapel"""

        tupladesc = ('us_id', 'us_name', 'us_nomapel', 'us_datecreated','us_status','estado')

        return self.all(sql, tupladesc)

    def find_byid(self, id_user):
        """
        Retorna un usuario en formato json
        :param id_user:
        :return:
        """
        sql = """
                select us_id, us_name, us_nomapel, us_datecreated, 
                case when us_status = 0 then 'ACTIVO' when us_status =1 then 'INACTIVO' else 'ND' end as estado 
                from tuser where us_id = {0}""".format(id_user)

        tupladesc = ('us_id', 'us_name', 'us_nomapel', 'us_datecreated', 'estado')

        return self.first(sql, tupladesc)

    def update_nomapel(self, id_user, nomapel, user_name, roles):
        """
        Actualiza el nombre del usuario
        :param id_user:
        :param us_nomapel:
        :return:
        """

        if not cadenas.es_nonulo_novacio(nomapel):
            raise ErrorValidacionExc("Debe ingresar los apellidos y nombres del usuario")

        if not cadenas.es_nonulo_novacio(user_name):
            raise ErrorValidacionExc("Debe ingresar el nombre de usuario")

        tuser = self.dbsession.query(TUser).filter(TUser.us_id == id_user).first()

        if tuser is not None:

            if cadenas.strip(user_name) != cadenas.strip(tuser.us_name):
                if self.existe(user_name):
                    raise ErrorValidacionExc(
                        "Ya existe una cuenta de usuario con el nombre:{0}, elija otro".format(user_name))

            tuser.us_nomapel = nomapel.upper()
            tuser.us_name = user_name

        # Registro de la matriz de roles
        tuserroldao = TUserRolDao(self.dbsession)
        tuserroldao.asociar(us_id=id_user, roles_list=roles)

    def resetPassword(self, id_user, password, rpassword):
        """
        Resetea un clave de un usuario y lo pone en estado como clave temporal
        :param id_user:
        :param password:
        :param rpassword:
        :return:
        """
        tuser = self.dbsession.query(TUser).filter(TUser.us_id == id_user).first()

        if tuser is not None:
            if not cadenas.es_nonulo_novacio(password):
                raise ErrorValidacionExc("Debe ingresar la clave inicial")
            if not cadenas.es_nonulo_novacio(rpassword):
                raise ErrorValidacionExc("Ingrese la confirmación de la clave")

            tuser.us_pass = password
            tuser.us_statusclave = 0

    def cambiarEstado(self, id_user):
        """
        Cambia el estado actual del usuario, si es 0 pone 1 y viceversa
        :param id_user:
        :return:
        """
        tuser = self.dbsession.query(TUser).filter(TUser.us_id == id_user).first()
        msg = ''
        if tuser is not None:
            if tuser.us_status == 0:
                tuser.us_status = 1
                msg = 'El usuario ha sido dado de baja'
            elif tuser.us_status == 1:
                tuser.us_status = 0
                msg = 'El usuario ha sido activado'


