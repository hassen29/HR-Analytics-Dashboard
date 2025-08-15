import { Routes } from '@angular/router';
import { Login } from './login/login';
import { Register } from './register/register';
import { Dashboard } from './dashboard/dashboard';
import { Recrutement } from './dashboard/recrutement/recrutement';
import { Predictjob } from './dashboard/recrutement/predictjob/predictjob';
import { ListCandidat } from './dashboard/recrutement/list-candidat/list-candidat';


export const routes: Routes = [
{path: '' ,redirectTo:'/dashboard', pathMatch: 'full'},



{ path: 'dashboard', component: Dashboard, children: [
    { path: 'recrutement', component: Recrutement, children: [
        {path: '' ,redirectTo:'list', pathMatch: 'full'},
        { path: 'predict', component: Predictjob },
        { path: 'list', component: ListCandidat }
    ]}
]},




{path: 'register' , component: Register},
{path: 'login' , component: Login},


];
