import Stage0 from './components/Stage0'
import Stage1 from './components/Stage1'
import Stage2 from './components/Stage2'
import Stage3 from './components/Stage3'
import Stage4 from './components/Stage4'
import Stage5 from './components/Stage5'
import Stage6 from './components/Stage6'
import Stage7 from './components/Stage7'

export default function App() {
  return (
    <div className="p-4 space-y-2">
      <h1 className="text-3xl font-bold mb-4">God Mode Ultra Flow</h1>
      <Stage0 />
      <Stage1 />
      <Stage2 />
      <Stage3 />
      <Stage4 />
      <Stage5 />
      <Stage6 />
      <Stage7 />
    </div>
  )
}
