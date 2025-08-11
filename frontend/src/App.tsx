// App entry with Stage 0 Ultra panel
import Stage0Panel from './components/Stage0Panel'
import Stage1 from './components/Stage1'
import Stage2 from './components/Stage2'
import Stage3 from './components/Stage3'
import Stage4 from './components/Stage4'
import Stage5 from './components/Stage5'
import Stage6 from './components/Stage6'
import Stage7 from './components/Stage7'
import Stage8 from './components/Stage8'
import Stage9 from './components/Stage9'
import Stage10 from './components/Stage10'
import Stage11 from './components/Stage11'

export default function App() {
  return (
    <div className="p-4 space-y-2">
      <h1 className="text-3xl font-bold mb-4">God Mode Ultra Flow</h1>
      <Stage0Panel />
      <Stage1 />
      <Stage2 />
      <Stage3 />
      <Stage4 />
      <Stage5 />
      <Stage6 />
      <Stage7 />
      <Stage8 />
      <Stage9 />
      <Stage10 />
      <Stage11 />
    </div>
  )
}
