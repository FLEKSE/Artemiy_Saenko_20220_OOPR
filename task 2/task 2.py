class Router():
    def __init__(self) -> None:
        i = 0                                
        while (i in Router.router_ip_list):  
            i += 1                           
        self.ip = i                         
        Router.router_ip_list.append(i) 
        self.linked_servers = {} 
        self.buffer = [] 
    
    def link(self, new_server) -> None:
        new_server.linked_router = self 
        self.linked_servers[int(f'{new_server.get_ip()}')] = new_server  

    def unlink(self, linked_server) -> None:
        linked_server.linked_router = None  
        self.linked_servers.pop(linked_server.get_ip())  

    def send_data(self) -> None:
        for mess in self.buffer: 
            if self.linked_servers.get(mess.receiver_ip) != None:
                 pass
            else:
                return None
            self.linked_servers.get(mess.receiver_ip).buffer.append(mess)
        self.buffer.clear()
            

    router_ip_list = []

class Server():
    def __init__(self) -> None:
        i = 0                                
        while (i in Server.server_ip_list): 
            i += 1
        self.ip = i 
        Server.server_ip_list.append(i)  
        self.linked_router = None  
        self.buffer = []  

    def send_data(self, mess) -> None:
        self.linked_router.buffer.append(mess) 

    def get_data(self) -> list:
        var_list = self.buffer.copy()  
        self.buffer.clear()  
        return var_list

    def get_ip(self) -> int:
        return self.ip

    server_ip_list = []
    
class Data():
    def __init__(self, mess: str, receiver_ip: int):
        self.data = mess
        self.receiver_ip = receiver_ip

# serv1 = Server()
# serv2 = Server()
# router1 = Router()

# router1.link(serv1)
# router1.link(serv2)

# serv1.send_data(Data("Hello", serv2.get_ip()))
# serv2.send_data(Data("Hi", serv1.get_ip()))
# router1.send_data()
# received_data1 = serv1.get_data()
# received_data2 = serv2.get_data()
# print(f'serv1 получил {received_data1[0].data}, serv2 получил {received_data2[0].data}')

assert hasattr(Router, 'link') and hasattr(Router, 'unlink') and hasattr(Router, 'send_data'), "в классе Router присутсвутю не все методы, указанные в задании"
assert hasattr(Server, 'send_data') and hasattr(Server, 'get_data') and hasattr(Server, 'get_ip'), "в классе Server присутсвутю не все методы, указанные в задании"
router = Router()
sv_from = Server()
sv_from2 = Server()
router.link(sv_from)
router.link(sv_from2)
router.link(Server())
router.link(Server())
sv_to = Server()
router.link(sv_to)
sv_from.send_data(Data("Hello", sv_to.get_ip()))
sv_from2.send_data(Data("Hello", sv_to.get_ip()))
sv_to.send_data(Data("Hi", sv_from.get_ip()))
router.send_data()
msg_lst_from = sv_from.get_data()
msg_lst_to = sv_to.get_data()
assert len(router.buffer) == 0, "после отправки сообщений буфер в роутере должен очищаться"
assert len(sv_from.buffer) == 0, "после получения сообщений буфер сервера должен очищаться"
assert len(msg_lst_to) == 2, "метод get_data вернул неверное число пакетов"
assert msg_lst_from[0].data == "Hi" and msg_lst_to[0].data == "Hello", "данные не прошли по сети, классы не функционируют должным образом"
assert hasattr(router, 'buffer') and hasattr(sv_to, 'buffer'), "в объектах классов Router и/или Server отсутствует локальный атрибут buffer"
router.unlink(sv_to)
sv_from.send_data(Data("Hello", sv_to.get_ip()))
router.send_data()
msg_lst_to = sv_to.get_data()
assert msg_lst_to == [], "метод get_data() вернул неверные данные, возможно, неправильно работает метод unlink()"
