import { AfterViewChecked, Component, ElementRef, Input, OnInit, ViewChild, ViewEncapsulation } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FileUploadModule } from 'primeng/fileupload';
import { MessageService, PrimeNGConfig } from 'primeng/api';
import { CardModule } from 'primeng/card';
import { ToastModule } from 'primeng/toast';
import { BadgeModule } from 'primeng/badge';
//import { ImportsModule } from './imports.ts';
import { FieldsetModule } from 'primeng/fieldset';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

import { CarouselModule } from 'primeng/carousel';
import { ButtonModule } from 'primeng/button';

import { DividerModule } from 'primeng/divider';
import { FloatLabelModule } from 'primeng/floatlabel';


import { PanelModule } from 'primeng/panel';
class Message {
	text?: string;
	type: MessageType;
	Style: string;
}

enum MessageType {
	Bot = 'chat-bubble chat-bubble--left',
	User = 'chat-bubble chat-bubble--right',
	Loading = 'chat-bubble-load loading'
}

@Component({
	standalone: true,
	imports: [FormsModule, CommonModule, FileUploadModule, CardModule, ToastModule, BadgeModule, CarouselModule, FieldsetModule, ButtonModule, DividerModule, PanelModule, FloatLabelModule],
	providers: [MessageService],
	selector: 'app-chatAgent',
	templateUrl: './chatAgent.component.html',
	styleUrls: ['./chatAgent.component.scss'],
	encapsulation: ViewEncapsulation.None
})
export class ChatAgentComponent implements OnInit, AfterViewChecked {
	//@ViewChild('messageContainer') private messageContainer: ElementRef;
	@Input() public display: string;

	public form: FormGroup;
	public messages: Array<Message> = [];
	public canSendMessage = true;

	constructor(private formBuilder: FormBuilder, private config: PrimeNGConfig, private messageService: MessageService, private httpClient: HttpClient) { }


	public actualUser = { "name": '', "lema": "", "hi": "", "image": "" }
	public chats: any[] = []

	public prompt = ""
	public loading = false
	public actualInx = 0

	ngOnInit(): void {

		this.form = this.formBuilder.group({
			message: ['']
		});

		this.chats = [{ "name": 'Peccy Bot', "lema": "Go FSI!", "hi": "Soy Peccy Bot, un experto en servicios financieros de AWS. Estoy aquí para ayudarte a revisar tus productos, realizar transacciones, consultar sobre nuevos productos u oportunidades de inversión", "image": "/chatAgent/bot.png" },
		]

		this.actualUser = this.chats[0]
		this.actualInx = 0;
		this.canSendMessage = false;
		const waitMessage: Message = { type: MessageType.Loading, Style: 'col-md-8' };
		this.messages.push(waitMessage);

		setTimeout(() => {
			this.messages.pop();
			const botMessage: Message = { text: this.actualUser.hi, type: MessageType.Bot, Style: 'col-md-8' };
			this.messages.push(botMessage);
			this.canSendMessage = true;
		}, 2000);


	}

	ngAfterViewChecked(): void {
		this.scrollToBottom();
	}

	public onClickSendMessage(): void {
		const info = this.prompt
		console.log("mesaje es: " + info)

		console.log("estado", this.canSendMessage)
		if (!this.canSendMessage) {
			const waitMessage: Message = { type: MessageType.Loading, Style: 'col-md-8' };
			this.messages.push(waitMessage);

			setTimeout(() => {
				this.messages.pop();
				const botMessage: Message = { text: 'Lo siento no estoy disponible', type: MessageType.Bot, Style: 'col-md-8' };
				this.messages.push(botMessage);
			}, 2000);
		}


		if (info && this.canSendMessage) {
			const userMessage: Message = { text: info, type: MessageType.User, Style: 'col-md-6 offset-md-6' };
			this.messages.push(userMessage);

			this.form.get('message').setValue('');
			this.form.updateValueAndValidity();
			this.generarRecomendacion()
		}
	}

	public message = []



	public loadNewChat(dataInd) {

		if (dataInd > 0) {
			this.canSendMessage = false
		} else this.canSendMessage = true


		this.actualInx = dataInd;

		this.messages = []
		this.actualUser = this.chats[dataInd];
		let waitMessage = { type: MessageType.Loading, Style: 'col-md-8' };
		this.messages.push(waitMessage);
		setTimeout(() => {
			this.messages.pop();
			const botMessage: Message = { text: this.actualUser.hi, type: MessageType.Bot, Style: 'col-md-8' };
			this.messages.push(botMessage);
		}, 2000);

	}




	public async generarRecomendacion() {

		this.canSendMessage = false;
		this.loading = true
		console.log("generando datos");
		let headers = new HttpHeaders({
			'Content-Type': 'application/json'
		});


		//let dataBody = {"promptBase": "", "imageBase":datosPay}


		/*var botMessage: Message = {text: "Primero validaré tu información, para verificar que sea correcta y soportada: ", type: MessageType.Bot, Style:'col-md-8'};
			 this.messages.push(botMessage);
		
		let validPrompt = 'validated if "'+ this.prompt+ '" request is valid according supported services and specifications if not return a tag <ERROR>'
		
		let dataBody = {"promptBase": validPrompt, "messages": this.message}
		
		let waitMessage: Message = {type: MessageType.Loading, Style:'col-md-8'};
		this.messages.push(waitMessage);
		
		let dataBodyRequest = {"promptBase": this.prompt, "messages": this.message}
		this.prompt = ""
		
		result = await this.httpClient.post<any>("https://nmanm7dmal.execute-api.us-east-1.amazonaws.com/prod/carbon", dataBody, { headers }).toPromise();
		
		
		this.messages.pop();
		if (result.body.Answer.includes('<ERROR>')){
			this.messages.pop();
			var info = result.body.Answer.replace('<ERROR>', '')
			info = info.replace('</ERROR>', '')
			 var botMessage: Message = {text: info, type: MessageType.Bot, Style:'col-md-8'};
			 this.messages.push(botMessage);
			this.canSendMessage = true;
			return
		}
		
		var botMessage: Message = {text: 'Listo, todo está correcto :D Ahora procederé con la respuesta:', type: MessageType.Bot, Style:'col-md-8'};
		this.messages.push(botMessage);
		*/
		//console.log("info es: "+JSON.stringify( dataBody))

		//let dataBodyRequest = {"promptBase": this.prompt, "messages": this.message} -> se eliminan los mensajes
		let dataBodyRequest = { "input": this.prompt, "from_number": "123456789" }
		this.prompt = ""

		let waitMessage = { type: MessageType.Loading, Style: 'col-md-8' };
		this.messages.push(waitMessage);
		let result = await this.httpClient.post<any>(
			"<FSI_ENDPOINT_REPLACE_ME>/invokemodel",
			dataBodyRequest,
			{ headers }
		).toPromise();
		console.log("resultado es: ", result)

		if (result.success != "true") {
			this.messages.pop();
			var botMessage: Message = { text: 'Disculpa aún estoy en construcción. Intenta de nuevo. Sorry I am still in building process. Please try again', type: MessageType.Bot, Style: 'col-md-8' };
			this.messages.push(botMessage);
			this.canSendMessage = true;
		}
		else {
			//this.ejec = true
			this.prompt = ""
			this.messages.pop();
			var resp = result.response
			//this.message = result.messages
			console.log("mensaje es: ", this.message)
			var botMessage: Message = { text: resp, type: MessageType.Bot, Style: 'col-md-8' };
			this.messages.push(botMessage);
			this.canSendMessage = true;
			/*console.log(resp.analisis)
			var botMessage: Message = {text: resp.analisis, type: MessageType.Bot};
			this.messages.push(botMessage);
		    
			botMessage= {text: resp.listaRecomendaciones, type: MessageType.Bot};
			this.messages.push(botMessage);
		   this.canSendMessage = true;
		   console.log(resp)*/
		}
		this.loading = false

	}

	private getBotMessage(): void {
		this.canSendMessage = false;
		const waitMessage: Message = { type: MessageType.Loading, Style: 'col-md-8' };
		this.messages.push(waitMessage);

		setTimeout(() => {
			this.messages.pop();
			const botMessage: Message = { text: 'Hola soy Peccy, cómo puedo ayudarte?', type: MessageType.Bot, Style: 'col-md-8' };
			this.messages.push(botMessage);
			this.canSendMessage = true;
		}, 2000);
	}

	public onClickEnter(event: KeyboardEvent): void {
		event.preventDefault();
		this.onClickSendMessage();
	}

	private scrollToBottom(): void {
		//this.messageContainer.nativeElement.scrollTop = this.messageContainer.nativeElement.scrollHeight;         
	}
}
