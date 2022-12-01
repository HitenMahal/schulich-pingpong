
export default function Sidebar({links,close,showSidebar}) {
    return (
        <div className={showSidebar ? "sidebar" : "sidebar off"} onClick={close}>
            {   links.map(links => (
                <a className="sidebar-link" href="#!" key={links.name}><links.icon />{links.name}</a>
            ))}
        </div>
    )
}