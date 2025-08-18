import { Routes } from '@angular/router';
import { Login } from './login/login';
import { Register } from './register/register';
import { Dashboard } from './dashboard/dashboard';
import { Recrutement } from './dashboard/recrutement/recrutement';
import { Predictjob } from './dashboard/recrutement/predictjob/predictjob';
import { ListCandidat } from './dashboard/recrutement/list-candidat/list-candidat';
import { Turnover } from './dashboard/turnover/turnover';
import { List } from './dashboard/turnover/list/list';
import { PredictAttrition } from './dashboard/turnover/predict-attrition/predict-attrition';
import { authGuard } from './guards/auth-guard';


export const routes: Routes = [
{path: '' ,redirectTo:'/dashboard', pathMatch: 'full'},



{ path: 'dashboard', component: Dashboard, canActivate: [authGuard],  children: [
    
    { path: 'recrutement', component: Recrutement, children: [
        {path: '' ,redirectTo:'list', pathMatch: 'full'},
        { path: 'predict', component: Predictjob },
        { path: 'list', component: ListCandidat }
    ]},


    { path: 'attrition', component: Turnover, children: [
        {path: '' ,redirectTo:'list', pathMatch: 'full'},
        { path: 'predict', component: PredictAttrition },
        { path: 'list', component: List }
    ]}
]},




{path: 'register' , component: Register},
{path: 'login' , component: Login},


];
