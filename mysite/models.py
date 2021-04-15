from django.db import models
from django.contrib.auth.models import User
from markdown import markdown
from django.utils.html import mark_safe

	 
class Prodotto(models.Model):

    nome = models.CharField(max_length=40, help_text='Inserisci il nome del prodotto')
    descrizione = models.CharField(max_length=40, help_text='Inserisci la descrizione del prodotto')
    stato = models.CharField(max_length=40, help_text='Inserisci lo stato del punto vendita del prodotto')
    via = models.CharField(max_length=40, help_text='Inserisci la via del punto vendita del prodotto')
    
    
    def __str__(self):
      
        return self.nome

        

                
class Commesse(models.Model):

    nome = models.CharField(max_length=40, help_text='Inserisci il nome della commessa')
    età = models.IntegerField(help_text='età commessa') 
    
    def __str__(self):
      
        return self.nome     

class Valutazione(models.Model):

    aspetto = models.IntegerField(help_text='Valuta il suo aspetto') 
    servizio = models.IntegerField(help_text='Valuta il servizio ricevuto') 
    commessa = models.ForeignKey(Commesse, help_text = 'Commessa', on_delete=models.CASCADE)

class Appunti(models.Model):

    appunto = models.CharField(max_length=40, help_text='Inserisci un appunto privato')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #da inserire per avere utente loggato e tenerne traccia
    
    
    def __str__(self):
      
        return self.appunto
        
        
#un esempio di qualcosa vicino alla tesi edificio --> servizi ---> voto

class Edificio(models.Model):
     nome = models.CharField(max_length=40, help_text='Inserisci il nome del edificio')
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     def __str__(self):
         return self.nome

         
class Servizi(models.Model):

     nome = models.CharField(max_length=40, help_text='Inserisci il nome del servizio')
     edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE) 
        
     def __str__(self):
         return self.nome
               	
class Voto(models.Model):
	comfort = models.IntegerField(help_text='Valuta il comfort del servizio ricevuto') 
	costo = models.IntegerField(help_text='Valuta il costo del servizio ricevuto') 
	edificio = models.ForeignKey(Servizi, on_delete=models.CASCADE)
       	

         
        	

	
