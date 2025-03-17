import { Routes } from '@angular/router';

import { ChatAgentComponent } from './paginas/chatAgent/chatAgent.component';

export const routes: Routes = [
  { path: '', component: ChatAgentComponent},
  { path: '**', component: ChatAgentComponent},
];




