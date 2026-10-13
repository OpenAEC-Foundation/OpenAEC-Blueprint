//! A consuming application: no copied shell code, CSS, JavaScript or Tauri.
use openaec_ui::{iced::{self, widget::{column, text, text_input}, Element, Task}, icons::Icon, *};

#[derive(Debug, Clone)]
enum Action { New, Rename(String), Save, SelectIcons, SelectWorkspace }
#[derive(Default)]
struct Studio { documents: Vec<Document>, active: Option<String>, next_id:u64, show_icons:bool, pending_close: Option<String> }
impl Studio {
    fn active(&self) -> Option<&Document> { self.documents.iter().find(|d|Some(&d.id)==self.active.as_ref()) }
}
impl Application for Studio {
    type Command=Action;
    fn title(&self)->String { "OpenAEC Studio · UI Library".into() }
    fn ribbon(&self,l:Language)->Vec<RibbonTab<Action>> {
        vec![
            RibbonTab { id:"home".into(),label:l.text("Start","Home").into(),groups:vec![
                RibbonGroup { label:l.text("Document","Document").into(),commands:vec![
                    Command::new(l.text("Nieuw","New"),Icon::New,Action::New),
                    Command::new(l.text("Opslaan (demo)","Save (demo)"),Icon::Save,Action::Save).enabled(self.active().is_some_and(|d|d.dirty)),
                ]},
                RibbonGroup { label:l.text("Bibliotheek","Library").into(),commands:vec![
                    Command::new(l.text("Werkruimte","Workspace"),Icon::Cube,Action::SelectWorkspace).selected(!self.show_icons),
                    Command::new(l.text("Iconen","Icons"),Icon::Grid,Action::SelectIcons).selected(self.show_icons),
                ]},
            ]},
        ]
    }
    fn workspace(&self,theme:Theme,l:Language)->Element<'_,Action> {
        if self.show_icons {
            let mut rows=column![text(l.text("Centrale iconen","Canonical icons")).font(fonts::HEADING).size(28)].spacing(16);
            for chunk in Icon::ALL.chunks(5) {
                let mut row=iced::widget::Row::new().spacing(24);
                for icon in chunk {
                    row=row.push(column![icon.view(24,theme.tokens().text),text(format!("{icon:?}")).size(11)].spacing(8).width(100).align_x(iced::Alignment::Center));
                }
                rows=rows.push(row);
            }
            return iced::widget::scrollable(iced::widget::container(rows).padding(32)).into();
        }
        match self.active() {
            None => widgets::empty_state(l.text("Bouw samen. Bouw open.","Build together. Build open."),l.text("Maak een document om de gedeelde UI te bekijken.","Create a document to explore the shared UI."),theme),
            Some(doc) => iced::widget::container(column![
                text(l.text("Werkruimte","Workspace")).font(fonts::HEADING).size(28),
                text(l.text("Documentnaam","Document name")).size(13),
                text_input(l.text("Naam","Name"),&doc.title).on_input(Action::Rename),
                text(l.text("Deze demo bewaart documenten alleen in het geheugen.","This demo keeps documents in memory only.")).size(12),
                text(if self.pending_close.is_some() {l.text("Sla het document op voordat je het sluit.","Save the document before closing it.")} else {""}).color(theme.tokens().danger_color),
            ].spacing(16).max_width(600)).padding(32).into(),
        }
    }
    fn explorer(&self,theme:Theme,_l:Language)->Element<'_,Action> {
        let mut list=column![].spacing(8);
        for doc in &self.documents { list=list.push(widgets::property(doc.title.clone(),if doc.dirty {"•"} else {""},theme)); }
        list.into()
    }
    fn properties(&self,theme:Theme,l:Language)->Element<'_,Action> {
        column![widgets::property(l.text("Documenten","Documents"),self.documents.len().to_string(),theme),widgets::property(l.text("Thema","Theme"),theme.to_string(),theme)].spacing(12).into()
    }
    fn update(&mut self,action:Action)->Task<Action> {
        match action {
            Action::New => { self.next_id+=1;let id=self.next_id.to_string();self.documents.push(Document{id:id.clone(),title:format!("Document {}",self.next_id),dirty:false});self.active=Some(id);self.show_icons=false; }
            Action::Rename(title) => { if let Some(doc)=self.documents.iter_mut().find(|d|Some(&d.id)==self.active.as_ref()) {doc.title=title;doc.dirty=true;} }
            Action::Save => {if let Some(doc)=self.documents.iter_mut().find(|d|Some(&d.id)==self.active.as_ref()){doc.dirty=false;}self.pending_close=None;}
            Action::SelectIcons => self.show_icons=true,
            Action::SelectWorkspace => self.show_icons=false,
        }
        Task::none()
    }
    fn documents(&self)->Vec<Document>{self.documents.clone()}
    fn active_document(&self)->Option<String>{self.active.clone()}
    fn file_commands(&self,l:Language)->Vec<Command<Action>> { self.ribbon(l).remove(0).groups.remove(0).commands }
    fn document_event(&mut self,event:DocumentEvent)->Task<Action> {
        match event {
            DocumentEvent::Activate(id) => {self.active=Some(id);self.show_icons=false;}
            DocumentEvent::CloseRequested(id) => {
                if self.documents.iter().any(|d|d.id==id && d.dirty) { self.pending_close=Some(id.clone());self.active=Some(id);self.show_icons=false; }
                else {self.documents.retain(|d|d.id!=id);if self.active.as_ref()==Some(&id){self.active=self.documents.last().map(|d|d.id.clone());}}
            }
        }
        Task::none()
    }
    fn close_requested(&mut self)->bool {
        if let Some(doc)=self.documents.iter().find(|d|d.dirty) {self.active=Some(doc.id.clone());self.pending_close=Some(doc.id.clone());self.show_icons=false;false} else {true}
    }
}
fn main()->iced::Result { run(Studio::default(),None) }
