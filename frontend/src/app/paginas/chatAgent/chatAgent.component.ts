import { AfterViewChecked, Component, Input, OnInit, ViewEncapsulation } from '@angular/core';
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
	Loading = 'chat-bubble-load loading',
	BotImg = 'image',
	BotPdf = 'pdf'
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
	public API_ENDPOINT: String = "";  // Dynamically loaded from "public/outputs.json"

	constructor(private formBuilder: FormBuilder, private config: PrimeNGConfig, private messageService: MessageService, private httpClient: HttpClient) { }


	public actualUser = { "name": '', "lema": "", "hi": "", "image": "" }
	public chats: any[] = []

	public prompt = ""
	public loading = false
	public actualInx = 0

	ngOnInit(): void {


		// LOAD API ENDPOINT DYNAMICALLY FROM "outputs.json" file
		// Load the outputs.json file
		this.httpClient.get<any>('outputs.json').subscribe(
			(data) => {
				this.API_ENDPOINT = data['fsi-multi-agents-backend-prod'].APIChatbot;
				console.log('Loaded API_ENDPOINT:', this.API_ENDPOINT);
			},
			(error) => {
				console.error('Failed to load API endpoint:', error);
			}
		);


		this.form = this.formBuilder.group({
			message: ['']
		});

		this.chats = [{ "name": 'Ruffy', "lema": "Go FSI!", "hi": "Soy Ruffy, un experto en servicios financieros de AWS. Estoy aquí para ayudarte a revisar tus productos, realizar transacciones, consultar sobre nuevos productos u oportunidades de inversión", "image": "/chatAgent/bot.png" },
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

		//let dataBodyRequest = {"promptBase": this.prompt, "messages": this.message} -> se eliminan los mensajes
		let dataBodyRequest = { "input": this.prompt, "from_number": "123456789" }
		this.prompt = ""

		let waitMessage = { type: MessageType.Loading, Style: 'col-md-8' };
		this.messages.push(waitMessage);
		let result = await this.httpClient.post<any>(
			`${this.API_ENDPOINT}`,
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

			// Detect message type (text, Image, PDF, etc...)
			let mesType = MessageType.Bot
			if (result.type == "image") mesType = MessageType.BotImg
			else if (result.type == "pdf") mesType = MessageType.BotPdf

			// Send message to chatbot
			var botMessage: Message = { text: resp, type: mesType, Style: 'col-md-8' };
			this.messages.push(botMessage);
			this.canSendMessage = true;

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
