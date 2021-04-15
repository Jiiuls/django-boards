from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponse
from mysite.models import Prodotto, Commesse, Valutazione, Appunti, Edificio, Servizi, Voto
from mysite.forms import ProdottoForm, CommesseForm, ValutazioneForm, AppuntiForm, EdificioForm, ServiziForm, VotoForm
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, DeleteView, FormView, UpdateView, ListView 
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User



class home(ListView):                #esempio su come riscrivere il codice per una tabella senza filtri
    model = Prodotto                 #nome del modello
    context_object_name = 'prodotto' #nome all'interno del context
    template_name = 'home.html'      #nome della pagina html, informazioni riprese dal codice sotto già implementato in precedenza ---> ricordati di aggiungere .as_view() negli urls.
    paginate_by = 5	             # --- > per impaginazione basta questo codice e nella pagina di template HTML
    	

        
        
#def home(request):
#	prodotto = Prodotto.objects.all()
#	context = {
#		"prodotto":prodotto
#	}
	
	
#	return render(request,'home.html',context)
	

class index(ListView):                                 #ecco come implementare le GCBV per le lista con restrizioni
    model = Prodotto
    context_object_name = 'prodotto'
    template_name = 'index.html'
    
    

    def get_queryset(self):
        self.prodotto = get_object_or_404(Prodotto, pk=self.kwargs.get('pk'))
        queryset = self.prodotto
        return queryset


#def index(request,pk):
#	prodotto = get_object_or_404(Prodotto, pk=pk)
#	context = {'prodotto':prodotto
#		   
#	}
#	return render(request,'index.html',context)
	
	
@method_decorator(login_required, name='dispatch')	     #non più come nell'esempio sotto, le GCBV necessitano di questo cambio metodo utilizzando method_decorator da importare da: 
class create_data(CreateView):                                                                    #from django.utils.decorators import method_decorator
    model = Prodotto
    form_class = ProdottoForm
    success_url = reverse_lazy('home')
    template_name = 'create_data.html'    

#@login_required	
#def create_data(request):
#    if request.method == 'POST':
#    	form = ProdottoForm(request.POST)
#    	if form.is_valid():
#        	form.save()
#        	return redirect('home')
#    else:
#    	form = ProdottoForm()
#
#    context = {
#    	'form':form
#    }
#    
#    return render(request, 'create_data.html', context) 


  
class commesse(ListView):
    model = Commesse
    context_object_name = 'commesse'
    template_name = 'commesse.html'   
       
#def commesse(request):
#	commesse = Commesse.objects.all()
#	context = {
#		'commesse':commesse
#	}
#	return render(request,'commesse.html',context)
	
@login_required	
def valutare(request, pk):
    commessa = get_object_or_404(Commesse, pk=pk)
    
    if request.method == 'POST':
        form = ValutazioneForm(request.POST)
        if form.is_valid():
            valutazione = form.save(commit=False)
            valutazione.commessa = commessa    #----> qui ho salvato il modello commessa selezionato in commessa del nuovo modello
            
            valutazione.save()
            
            return redirect('commesse')  
    else:
        form = ValutazioneForm()
    return render(request,'valutare.html', {'form': form}) #---> qui c'è da passare il nome utilizzato per la funzione del forms.py



class nuova_commessa(CreateView):
    model = Prodotto
    form_class = CommesseForm
    success_url = reverse_lazy('commesse')
    template_name = 'nuova_commessa.html'   


#@login_required	
#def nuova_commessa(request):
#    if request.method == 'POST':
#    	form = CommesseForm(request.POST)
#    	if form.is_valid():
#        	form.save()
#        	return redirect('commesse')
#    else:
#    	form = CommesseForm()
#
#    context = {
#    		'form':form,
#    	}
#    
#    return render(request, 'nuova_commessa.html', context)  



def dettagli(request, pk):
	commessa = get_object_or_404(Commesse, pk=pk)
	dettaglio = list(Valutazione.objects.filter(commessa=commessa))
	
	
	context = {
		'dettaglio':dettaglio
	}
	return render(request,'dettagli.html',context)


@login_required	
def appunti(request):
    appunti = list(Appunti.objects.filter(user=request.user)) #codice da usare se non è sicuro che la lista sia piena! non da errori se vuota
    page = request.GET.get('page',1)
    paginator = Paginator(appunti, 2) 
    
    try:
        appunti = paginator.page(page)   #dai il nome della lista che vuoi mostrare (ovvero appunti) --> riscrivendo il codice su codice già fatto è comodo da ricordare nb c'è il codice poi di
      							#impaginazione che ti metto negli appunti (lo vedi anche nella pagina html appunti.html (codice per impaginazione per FBV)
      							#c'è anche quello per GCBV che vedi nelle views GCBV
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        appunti = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        appunti = paginator.page(paginator.num_pages)
    context = {
		"appunti":appunti,
		
		
	}
	
	
    return render(request,'appunti.html',context)



@login_required	
def nuovo_appunto(request):  #codice per salvare l'utente loggato 
    
    
    if request.method == 'POST':
        form = AppuntiForm(request.POST)
        if form.is_valid():
            appunto = form.save(commit=False)
            appunto.user = request.user    #in form non metto user cosi non me lo chiederà e prima di salvare il tutto aggiungo request.user, per il resto è uguale al codice sopra
            
            appunto.save()
            
            return redirect('appunti')  
    else:
        form = AppuntiForm()
    context = {
    		'form':form,
    	}
    return render(request,'nuovo_appunto.html', context) 
    
    
#ora proviamo ad entrare più nel dettaglio e a visualizzare il post scelto di un determinato user e modificarlo avendo di default il dato già salvato

class modifica_appunto(UpdateView):
    model = Appunti
    form_class = AppuntiForm
    template_name = 'modifica_appunto.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'appunto'

    def form_valid(self, form):
        appunto = form.save(commit=False)
        appunto.user = self.request.user
        appunto.save()
        return redirect('appunti')


#def modifica_appunto(request,pk):
#    appunto = get_object_or_404(Appunti, pk=pk)
#    if request.method == 'POST':
#        form = AppuntiForm(request.POST, instance = appunto)
#        if form.is_valid():
#            appunto = form.save(commit=False)
#            appunto.user = request.user
#            
#            
#            appunto.save()
#            
#            return redirect('appunti')  
#    else:
#        form = AppuntiForm(instance = appunto)
#    context = {
#    		'form':form,
#    	}
#    return render(request,'modifica_appunto.html', context)        


def elimina_appunto(request,pk):
    appunto = get_object_or_404(Appunti, pk=pk)
    if request.method == 'POST':
        form = AppuntiForm(request.POST, instance = appunto)
        if form.is_valid():
            appunto = form.save(commit=False)
            appunto.user = request.user
            
            
            appunto.delete()
            
            return redirect('appunti')  
    else:
        form = AppuntiForm(instance = appunto)
    context = {
    		'form':form,
    	}
    return render(request,'elimina_appunto.html', context)  
   
    




#ora proviamo a fare sta views complessa

@login_required	
def nuovo_edificio(request):  #codice per salvare l'utente loggato 
    
    
    if request.method == 'POST':
        form = EdificioForm(request.POST)
        if form.is_valid():
            edificio = form.save(commit=False)
            edificio.user = request.user    #in form non metto user cosi non me lo chiederà e prima di salvare il tutto aggiungo request.user, per il resto è uguale al codice sopra
            
            edificio.save()
            
            return redirect('lista_edifici')  
    else:
        form = EdificioForm()
    context = {
    		'form':form,
    	}
    return render(request,'nuovo_edificio.html', context)


@login_required	
def lista_edifici(request):
	edificio = list(Edificio.objects.filter(user=request.user)) #codice da usare se non è sicuro che la lista sia piena! non da errori se vuota
	servizi = Servizi.objects.all()
	
	
	
	return render(request,'lista_edifici.html', {"edificio" : edificio, "servizi" : servizi})
	
	

def servizi(request,pk):  
    
    edificio = get_object_or_404(Edificio, pk=pk)
    if request.method == 'POST':
        form = ServiziForm(request.POST)
        if form.is_valid():
            servizio = form.save(commit=False)
            servizio.edificio = edificio
            
            servizio.save()
            
            return redirect('lista_edifici')  
    else:
        form = ServiziForm()
    context = {
    		'form':form,
    	}
    return render(request,'servizi.html', context) 


def voto(request, pk): 
	voto = list(Voto.objects.filter(pk=pk)) #voti per il servizio pk 
	
	
	context = {
		"voto":voto,
		
		
	}
	
	
	return render(request,'voto.html',context)
	
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'my_account.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user













































